from django.conf.urls import url

from .views import CustomObtainAuthToken

app_name = 'gsauthentication'

urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
]
