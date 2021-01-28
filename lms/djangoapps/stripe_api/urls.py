from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_customer_id
from rest_framework import routers

urlpatterns = [
    path('get_customer_id/', get_customer_id)
]
