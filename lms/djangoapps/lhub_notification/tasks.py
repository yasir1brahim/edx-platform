from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime, timedelta
from django.conf import settings
from lms.djangoapps.lhub_notification.models import Notification
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from student.models import CourseEnrollment


cron_not_active_notification_settings = {
    'minute': '0',
    'hour': '1',
    'day_of_month': '*',
    'day_of_week': '*',
    'month_of_year': '*',
}


@periodic_task(run_every=crontab(**cron_not_active_notification_settings))
def create_not_active_notification():
    days_warning = 3

    try:
        main_site_conf = SiteConfiguration.objects.get(site__id=settings.SITE_ID)
    except SiteConfiguration.DoesNotExist:
        pass
    else:
        days_warning = main_site_conf.get_value('NOT_ACTIVE_DAYS', days_warning)

    microsites_conf = SiteConfiguration.objects.exclude(site__id=settings.SITE_ID)
    exclude_organisations = []

    for configuration in microsites_conf:
        course_org_list = configuration.get_value('course_org_filter')

        if not course_org_list:
            continue

        if not isinstance(course_org_list, list):
            course_org_list = [course_org_list]

        exclude_organisations.extend(course_org_list)
        microsite_days_warning = configuration.get_value('NOT_ACTIVE_DAYS', days_warning)
        microsite_target_date = datetime.now() - timedelta(days=microsite_days_warning)
        microsite_day_start = microsite_target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        microsite_day_end = microsite_day_start + timedelta(days=1)
        enrolled_users_data = CourseEnrollment.objects.filter(
            is_active=True,
            created__range=(microsite_day_start, microsite_day_end),
            course__org__in=course_org_list
        ).select_related('user', 'course')

        [Notification.create_not_active_notification(enrollment, microsite_days_warning)
         for enrollment in enrolled_users_data]

    target_date = datetime.now() - timedelta(days=days_warning)
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    enrolled_users_data = CourseEnrollment.objects.filter(
        is_active=True,
        created__range=(day_start, day_end),
    ).exclude(
        course__org__in=exclude_organisations
    ).select_related('user', 'course')

    [Notification.create_not_active_notification(enrollment, days_warning) for enrollment in enrolled_users_data]


cron_first_not_completed_notification_settings = {
    'minute': '0',
    'hour': '2',
    'day_of_month': '*',
    'day_of_week': '*',
    'month_of_year': '*',
}


@periodic_task(run_every=crontab(**cron_first_not_completed_notification_settings))
def create_first_not_completed_notification():
    days_warning = 7
    notification_type = Notification.FIRST_NOT_COMPLETED
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        main_site_conf = SiteConfiguration.objects.get(site__id=settings.SITE_ID)
    except SiteConfiguration.DoesNotExist:
        pass
    else:
        days_warning = main_site_conf.get_value('FIRST_NOT_COMPLETED_DAYS', days_warning)

    microsites_conf = SiteConfiguration.objects.exclude(site__id=settings.SITE_ID)
    exclude_organisations = []

    for configuration in microsites_conf:
        course_org_list = configuration.get_value('course_org_filter')

        if not course_org_list:
            continue

        if not isinstance(course_org_list, list):
            course_org_list = [course_org_list]

        exclude_organisations.extend(course_org_list)
        microsite_days_warning = configuration.get_value('FIRST_NOT_COMPLETED_DAYS', days_warning)
        microsite_target_date = today + timedelta(days=microsite_days_warning)
        day_start = microsite_target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        enrolled_users_data = CourseEnrollment.objects.filter(
            is_active=True,
            course__end_date__range=(day_start, day_end),
            course__org__in=course_org_list
        ).select_related('user', 'course')

        [Notification.create_not_completed_notification(enrollment, microsite_days_warning, notification_type)
         for enrollment in enrolled_users_data]

    target_date = today + timedelta(days=days_warning)
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    enrolled_users_data = CourseEnrollment.objects.filter(
        is_active=True,
        course__end_date__range=(day_start, day_end)
    ).exclude(
        course__org__in=exclude_organisations
    ).select_related('user', 'course')

    [Notification.create_not_completed_notification(enrollment, days_warning, notification_type)
     for enrollment in enrolled_users_data]


cron_second_not_completed_notification_settings = {
    'minute': '0',
    'hour': '3',
    'day_of_month': '*',
    'day_of_week': '*',
    'month_of_year': '*',
}


@periodic_task(run_every=crontab(**cron_second_not_completed_notification_settings))
def create_second_not_completed_notification():
    days_warning = 3
    notification_type = Notification.SECOND_NOT_COMPLETED
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        main_site_conf = SiteConfiguration.objects.get(site__id=settings.SITE_ID)
    except SiteConfiguration.DoesNotExist:
        pass
    else:
        days_warning = main_site_conf.get_value('SECOND_NOT_COMPLETED_DAYS', days_warning)

    microsites_conf = SiteConfiguration.objects.exclude(site__id=settings.SITE_ID)
    exclude_organisations = []

    for configuration in microsites_conf:
        course_org_list = configuration.get_value('course_org_filter')

        if not course_org_list:
            continue

        if not isinstance(course_org_list, list):
            course_org_list = [course_org_list]

        exclude_organisations.extend(course_org_list)
        microsite_days_warning = configuration.get_value('SECOND_NOT_COMPLETED_DAYS', days_warning)
        microsite_target_date = today + timedelta(days=microsite_days_warning)
        day_start = microsite_target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        enrolled_users_data = CourseEnrollment.objects.filter(
            is_active=True,
            course__end_date__range=(day_start, day_end),
            course__org__in=course_org_list
        ).select_related('user', 'course')

        [Notification.create_not_completed_notification(enrollment, microsite_days_warning, notification_type)
         for enrollment in enrolled_users_data]

    target_date = today + timedelta(days=days_warning)
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    enrolled_users_data = CourseEnrollment.objects.filter(
        is_active=True,
        course__end_date__range=(day_start, day_end)
    ).exclude(
        course__org__in=exclude_organisations
    ).select_related('user', 'course')

    [Notification.create_not_completed_notification(enrollment, days_warning, notification_type)
     for enrollment in enrolled_users_data]
