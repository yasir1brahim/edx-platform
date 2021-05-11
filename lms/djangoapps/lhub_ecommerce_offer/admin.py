from django.contrib import admin
from .models import Offer
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
import logging


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
        'course'
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
        'courses_sku'
    ]


    def courses_sku(self, obj):
        # return "\n".join([a.course_sku for a in obj.CourseOverview.all()])
        # for a in obj.CourseOverview.all():
        pass


admin.site.register(Offer, OfferAdmin)