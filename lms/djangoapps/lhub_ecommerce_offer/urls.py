from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import Ecommerce_Offer


urlpatterns = [
    url(r'^add/', Ecommerce_Offer.as_view(), name="lhub_ecommerce_offer"),
    url(r'^delete/(?P<offer_id>[0-9]+)$', Ecommerce_Offer.as_view(), name="lhub_ecommerce_offer")
]

