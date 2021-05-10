from django.contrib import admin
from .models import Offer

# Register your models here.

class OfferAdmin(admin.ModelAdmin):
    """ Admin class for Offer model """
    fields = (
        'incentive_type',
        'incentive_value',
        'condition_type',
        'condition_value',
        'start_datetime',
        'end_datetime',
        'priority',
        'is_exclusive',
        'associated_ecommerce_offer_id',
        # 'course'
    )
    list_display = [
        'incentive_type',
        'incentive_value',
        'condition_type',
        'condition_value',
        'start_datetime',
        'end_datetime',
        'priority',
        'is_exclusive',
        'associated_ecommerce_offer_id',
        # 'course'
    ]


admin.site.register(Offer, OfferAdmin)