from django.contrib import admin
from .models import Offer, Course

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
        'associated_ecommerce_offer_id'
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
        'associated_ecommerce_offer_id'
    ]

class CourseAdmin(admin.ModelAdmin):
    """ Admin class for Course model """
    fields = ('course',)
    list_display = ['course']


admin.site.register(Offer, OfferAdmin)
admin.site.register(Course, CourseAdmin)