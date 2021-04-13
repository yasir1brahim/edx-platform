from django.contrib import admin

from lms.djangoapps.lhub_notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'is_read', 'is_delete']
    list_filter = ['is_read', 'is_delete', 'notification_type']


admin.site.register(Notification, NotificationAdmin)
