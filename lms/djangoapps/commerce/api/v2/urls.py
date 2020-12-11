"""
Commerce URLs
"""


from django.conf import settings
from django.conf.urls import include, url

from . import views

COURSE_URLS = ([
    url(r'^$', views.CourseListView.as_view(), name='list'),
], 'courses')

app_name = 'v2'

urlpatterns = [
    url(r'^courses/', include(COURSE_URLS)),
]
