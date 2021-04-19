from django.contrib import admin
from .models import MobileUserSessionCookie

class MobileUserSessionCookieAdmin(admin.ModelAdmin):
    """ Admin class for MobileUserSessionCookie model """
    fields = ('user', 'session_cookie')
    list_display = ['user', 'session_cookie']

admin.site.register(MobileUserSessionCookie, MobileUserSessionCookieAdmin)
