from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from lms.djangoapps.lhub_notification import views


router = DefaultRouter()
router.register(r'api/notifications', views.NotificationViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^notifications/$', views.NotificationListView.as_view(),
        name='lhub-notification-list'),
    url(r'^notifications/(?P<pk>[^/]*)/$', views.NotificationDetail.as_view(),
        name='lhub-notification-detail'),
]
