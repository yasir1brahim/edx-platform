from django.conf.urls import url
from lms.djangoapps.lhub_extended_api import views

urlpatterns = [
    url(r'^orders$', views.LHUBOrdersHistoryView.as_view()),
]
