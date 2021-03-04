from django.db import models
from django.contrib.auth.models import User


class MobileUserSessionCookie(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    session_cookie = models.CharField(max_length=255, db_index=True)

    class Meta(object):
        app_label = "lhub_mobile"

