from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_customer_id, checkout_payment, custom_basket, basket_item_count, basket_buy_now, basket_buy_now_cancel, checkout_payment_intent, \
             confirm_payment_intent
from rest_framework import routers

urlpatterns = [
    path('get_customer_id/', get_customer_id),
    path('checkout_payment/', checkout_payment),
    path('checkout_payment_intent/', checkout_payment_intent),
    path('confirm_payment_intent/', confirm_payment_intent),
    path('basket/remove_item/', custom_basket),
    path('basket/count_item/', basket_item_count),
    path('basket/buy_now/', basket_buy_now),
    path('basket/buy_now/cancel/', basket_buy_now_cancel),
]
