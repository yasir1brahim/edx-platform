from django.conf import settings
from django.db import models
from openedx.core.djangoapps.content.course_overviews.models import Category

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UserExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True, related_name='user_extra_info',
        on_delete=models.CASCADE)

    nric = models.CharField(
        verbose_name="NRIC",
        max_length=100,
        blank=True,
        null=True
    )
    industry = models.ForeignKey(Category, related_name='users_industry', 
        on_delete=models.SET_NULL, null=True)
