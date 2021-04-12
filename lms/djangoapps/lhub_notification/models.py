from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from common.djangoapps.student.models import EnrollStatusChange
from common.djangoapps.student.signals import ENROLL_STATUS_CHANGE
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class Notification(TimeStampedModel):
    ENROLLMENT = 'enrollment'

    TYPE_CHOICES = (
        (ENROLLMENT, _('Enrollment')),
    )

    notification_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='lhub_notifications')
    course = models.ForeignKey(CourseOverview, null=True, on_delete=models.CASCADE)
    title = models.TextField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    @property
    def num_new_notifications(self):
        return Notification.objects.filter(
            user=self.user,
            is_delete=False,
            is_read=False
        ).count()


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
        title = u'You are enrolled in {}'.format(display_name)
        message = u'<p>Congratulations! You can now start learning your new course {}</p>' \
                  u'<p>You can browse through the course overview and progress through ' \
                  u'the course by completing chapters and quizzes. ' \
                  u'Completing this course will award you with a Certificate of Achievement!</p>'.format(
            display_name,
        )

        Notification.objects.create(
            user=user,
            course=course,
            notification_type=Notification.ENROLLMENT,
            title=title,
            message=message
        )
