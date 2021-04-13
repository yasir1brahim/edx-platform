"""
This file contains celery tasks for credentials-related functionality.
"""

import math
import time

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from edx_django_utils.monitoring import set_code_owner_attribute
from opaque_keys.edx.keys import CourseKey
from MySQLdb import OperationalError

from openedx.core.djangoapps.credentials.utils import get_credentials_api_client
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from lms.djangoapps.certificates.api import get_recently_modified_certificates
from lms.djangoapps.grades.api import get_recently_modified_grades
from lms.djangoapps.certificates.models import CertificateStatuses
from openedx.core.djangoapps.programs.signals import handle_course_cert_changed, handle_course_cert_awarded

logger = get_task_logger(__name__)

# Maximum number of retries before giving up.
# For reference, 11 retries with exponential backoff yields a maximum waiting
# time of 2047 seconds (about 30 minutes). Setting this to None could yield
# unwanted behavior: infinite retries.
MAX_RETRIES = 11


@shared_task(bind=True, ignore_result=True)
@set_code_owner_attribute
def send_grade_to_credentials(self, username, course_run_key, verified, letter_grade, percent_grade):
    """ Celery task to notify the Credentials IDA of a grade change via POST. """
    logger.info(f"Running task send_grade_to_credentials for username {username} and course {course_run_key}")

    countdown = 2 ** self.request.retries
    course_key = CourseKey.from_string(course_run_key)

    try:
        credentials_client = get_credentials_api_client(
            User.objects.get(username=settings.CREDENTIALS_SERVICE_USERNAME),
            org=course_key.org,
        )

        credentials_client.grades.post({
            'username': username,
            'course_run': str(course_key),
            'letter_grade': letter_grade,
            'percent_grade': percent_grade,
            'verified': verified,
        })

        logger.info(f"Sent grade for course {course_run_key} to user {username}")

    except Exception as exc:
        error_msg = f"Failed to send grade for course {course_run_key} to user {username}."
        logger.exception(error_msg)
        exception = MaxRetriesExceededError(
            f"Failed to send grade to credentials. Reason: {error_msg}"
        )
        raise self.retry(exc=exception, countdown=countdown, max_retries=MAX_RETRIES)


@shared_task(bind=True, ignore_result=True)
@set_code_owner_attribute
def handle_notify_credentials(self, options, course_keys):
    """
    Celery task to handle the notify_credentials management command. Finds the
    relevant cert and grade records, then starts other celery tasks to send the
    data.
    """

    try:
        site_config = SiteConfiguration.objects.get(site__domain=options['site']) if options['site'] else None
    except SiteConfiguration.DoesNotExist:
        logger.error('No site configuration found for site %s', options['site'])

    certs = get_recently_modified_certificates(
        course_keys, options['start_date'], options['end_date'], options['user_ids']
    )

    users = None
    if options['user_ids']:
        users = User.objects.filter(id__in=options['user_ids'])

    grades = get_recently_modified_grades(
        course_keys, options['start_date'], options['end_date'], users
    )

    logger.info('notify_credentials Sending notifications for {certs} certificates and {grades} grades'.format(
        certs=certs.count(),
        grades=grades.count()
    ))

    if options['dry_run']:
        print_dry_run(certs, grades)
    else:
        send_notifications(
            certs,
            grades,
            site_config=site_config,
            delay=options['delay'],
            page_size=options['page_size'],
            verbose=options['verbose'],
            notify_programs=options['notify_programs']
        )

    logger.info('notify_credentials finished')


def send_notifications(
    certs, grades, site_config=None, delay=0, page_size=100, verbose=False, notify_programs=False
):
    """ Run actual handler commands for the provided certs and grades. """

    # Imported here instead of above to avoid circular import
    from openedx.core.djangoapps.credentials.signals import send_grade_if_interesting

    course_cert_info = {}
    # First, do certs
    for i, cert in paged_query(certs, delay, page_size):
        if site_config and not site_config.has_org(cert.course_id.org):
            logger.info("Skipping credential changes %d for certificate %s", i, certstr(cert))
            continue

        logger.info(
            "Handling credential changes %d for certificate %s",
            i, certstr(cert),
        )

        signal_args = {
            'sender': None,
            'user': cert.user,
            'course_key': cert.course_id,
            'mode': cert.mode,
            'status': cert.status,
            'verbose': verbose,
        }

        data = {
            'mode': cert.mode,
            'status': cert.status
        }

        course_cert_info[(cert.user.id, str(cert.course_id))] = data
        handle_course_cert_changed(**signal_args)
        if notify_programs and CertificateStatuses.is_passing_status(cert.status):
            handle_course_cert_awarded(**signal_args)

    # Then do grades
    for i, grade in paged_query(grades, delay, page_size):
        if site_config and not site_config.has_org(grade.course_id.org):
            logger.info("Skipping grade changes %d for grade %s", i, gradestr(grade))
            continue

        logger.info(
            "Handling grade changes %d for grade %s",
            i, gradestr(grade),
        )

        user = User.objects.get(id=grade.user_id)

        # Grab mode/status from cert call
        key = (user.id, str(grade.course_id))
        cert_info = course_cert_info.get(key, {})
        mode = cert_info.get('mode', None)
        status = cert_info.get('status', None)

        send_grade_if_interesting(
            user,
            grade.course_id,
            mode,
            status,
            grade.letter_grade,
            grade.percent_grade,
            verbose=verbose
        )


def paged_query(queryset, delay, page_size):
    """
    A generator that iterates through a queryset but only resolves chunks of it at once, to avoid overwhelming memory
    with a giant query. Also adds an optional delay between yields, to help with load.
    """
    count = queryset.count()
    pages = int(math.ceil(count / page_size))

    for page in range(pages):
        page_start = page * page_size
        page_end = page_start + page_size
        subquery = queryset[page_start:page_end]

        if delay and page:
            time.sleep(delay)
        index = 0
        try:
            for item in subquery.iterator():
                index += 1
                yield page_start + index, item
        except OperationalError:
            # When running the notify_credentials command locally there is an
            # OperationalError thrown by MySQL when there are no more results
            # available for the queryset iterator. This change catches that exception,
            # checks state, and then logs according to that state. This code runs in
            # production without issue. This changes allows for the code to be run
            # locally without a separate code path.
            if index == count:
                logger.info('OperationalError Exception caught, all known results processed in paged_query')
            else:
                logger.warning('OperationalError Exception caught, it is possible some results were missed')
            continue

def print_dry_run(certs, grades):
    """Give a preview of what certs/grades we will handle."""
    print("DRY-RUN: This command would have handled changes for...")
    ITEMS_TO_SHOW = 10

    print(certs.count(), "Certificates:")
    for cert in certs[:ITEMS_TO_SHOW]:
        print("   ", certstr(cert))
    if certs.count() > ITEMS_TO_SHOW:
        print("    (+ {} more)".format(certs.count() - ITEMS_TO_SHOW))

    print(grades.count(), "Grades:")
    for grade in grades[:ITEMS_TO_SHOW]:
        print("   ", gradestr(grade))
    if grades.count() > ITEMS_TO_SHOW:
        print("    (+ {} more)".format(grades.count() - ITEMS_TO_SHOW))


def certstr(cert):
    return f'{cert.course_id} for user {cert.user.username}'


def gradestr(grade):
    return f'{grade.course_id} for user {grade.user_id}'
