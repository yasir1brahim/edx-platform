from django.urls import path
from django.conf.urls import url

from .views import UserSessionCookieView


GETVIEW = UserSessionCookieView.as_view({
    'get': 'get',
})



urlpatterns = [
#    path('', views.index, name='index'),
    url(
        r'^getSessionCookie/$',
        GETVIEW,
        name='get_user_cookie_api'
    ),
]
