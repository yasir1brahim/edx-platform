from django.conf.urls import url
from .views import create_review

urlpatterns = [
    url(r"^create_review/$", create_review, name='create_review'),
]
