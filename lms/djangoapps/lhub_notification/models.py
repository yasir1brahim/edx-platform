from completion.models import BlockCompletion
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from lms.djangoapps.course_blocks.api import get_course_blocks
from model_utils.models import TimeStampedModel

from common.djangoapps.student.models import EnrollStatusChange
from common.djangoapps.student.signals import ENROLL_STATUS_CHANGE
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from xmodule.modulestore.django import modulestore


class Notification(TimeStampedModel):
    ENROLLMENT = 'enrollment'
    NOT_ACTIVE = 'not_active'
    FIRST_NOT_COMPLETED = 'first_not_completed'
    SECOND_NOT_COMPLETED = 'second_not_completed'

    TYPE_CHOICES = (
        (ENROLLMENT, _('Enrollment')),
        (NOT_ACTIVE, _('Not active')),
        (FIRST_NOT_COMPLETED, _('First not completed')),
        (SECOND_NOT_COMPLETED, _('Second not completed')),
    )

    notification_type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='lhub_notifications')
    course = models.ForeignKey(CourseOverview, null=True, on_delete=models.CASCADE)
    title = models.TextField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    days_warning = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    @property
    def num_new_notifications(self):
        return Notification.objects.filter(
            user=self.user,
            is_delete=False,
            is_read=False
        ).count()

    @classmethod
    def create_not_active_notification(cls, enrollment, days_warning):
        course = enrollment.course
        user = enrollment.user
        has_progress = BlockCompletion.objects.filter(
            user=user,
            context_key=course.id
        ).exists()

        if not has_progress:
            display_name = course.display_name_with_default
            title = _(f'You enrolled in {display_name} {days_warning} days ago, start learning today!')
            message = _(f'<p>You enrolled in {display_name} on {enrollment.created.date()}, '
                        f'what are you waiting for?</p><p>You can browse through the course overview '
                        f'and progress through the course by completing chapters and quizzes. '
                        f'Completing this course will award you with a Certificate of Achievement!</p>')

            cls.objects.create(
                user=user,
                course=course,
                notification_type=cls.NOT_ACTIVE,
                title=title,
                message=message,
                days_warning=days_warning
            )

    @classmethod
    def create_not_completed_notification(cls, enrollment, days_warning, notification_type):
        course = enrollment.course
        user = enrollment.user
        store = modulestore()
        course_usage_key = store.make_course_usage_key(course.id)
        block_data = get_course_blocks(user, course_usage_key, include_completion=True)
        is_not_completed = False

        for section_key in block_data.get_children(course_usage_key):
            if not block_data.get_xblock_field(section_key, 'complete', False):
                is_not_completed = True
                break

        if is_not_completed:
            display_name = course.display_name_with_default
            title = _(f'{display_name} will be expiring in {days_warning} days! '
                      f'Complete it before your access to the course is removed on {course.end_date.date()}.')
            message = _(f'<p>{display_name} is expiring on {course.end_date.date()}, {days_warning} from today!</p>'
                        f'<p>Complete the course before your access is removed to receive your '
                        f'Certificate of Achievement. Once it expires, you will no longer be able to '
                        f'access course materials.</p>')

            cls.objects.create(
                user=user,
                course=course,
                notification_type=notification_type,
                title=title,
                message=message,
                days_warning=days_warning
            )


@receiver(ENROLL_STATUS_CHANGE)
def create_notification_on_enrollment(sender, event=None, user=None, course_id=None,
                                      **kwargs):  # pylint: disable=unused-argument
    """
    Create a notification to the given user a new enrollment
    """
    if event == EnrollStatusChange.enroll:
        course = CourseOverview.objects.filter(id=course_id).first()

        if course is None:
            return

        display_name = course.display_name_with_default
        title = _(f'You are enrolled in {display_name}')
        message = _(f'<p>Congratulations! You can now start learning your new course {display_name}</p>'
                    f'<p>You can browse through the course overview and progress through '
                    f'the course by completing chapters and quizzes. '
                    f'Completing this course will award you with a Certificate of Achievement!</p>')

        Notification.objects.create(
            user=user,
            course=course,
            notification_type=Notification.ENROLLMENT,
            title=title,
            message=message
        )
