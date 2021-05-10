from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import Ecommerce_Offer
# from oscar.core.loading import get_class


urlpatterns = [
    path('', Ecommerce_Offer.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)