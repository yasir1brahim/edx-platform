
from django.contrib.auth.models import User
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class CourseReview(models.Model):
    """
    Course Review in EdX System.
    User can create a feedback only after purchasing that course.
    User can only give feedback once, cannot give feedback again after first feedback.
    """

    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    course_id = models.ForeignKey(CourseOverview, db_index=True, on_delete=models.CASCADE)

    rating = models.DecimalField(default=1.0, max_digits=2, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    review = models.CharField(null=True, blank=True, max_length=1000)

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course Review'
        verbose_name_plural = 'Course Reviews'
        constraints = [
            models.UniqueConstraint(
                name='course_review_uniqueness',
                fields=['user_id', 'course_id'],
            )
        ]

