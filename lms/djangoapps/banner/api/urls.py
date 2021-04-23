"""
URLs for banner API
"""


from django.conf.urls import url

from .views import BannerApi

urlpatterns = [
    url('^details/$', BannerApi.as_view(), name='banner_api'),
]
