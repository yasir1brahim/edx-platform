from django.db import models
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview



class Offer(models.Model):
    incentive_type = models.CharField(max_length=250)
    incentive_value = models.DecimalField(max_digits=12, decimal_places=2)
    condition_type = models.CharField(max_length=250)
    condition_value = models.DecimalField(max_digits=12, decimal_places=2)
    start_datetime = models.DateTimeField('start datetime')
    end_datetime = models.DateTimeField('end datetime', null=True ,blank=True)
    priority = models.IntegerField()
    is_exclusive = models.BooleanField()
    associated_ecommerce_offer_id = models.IntegerField()
    course = models.ManyToManyField(CourseOverview)
    is_suspended = models.BooleanField(default=False)
    
    class Meta(object):
        app_label = "lhub_ecommerce_offer"



class Coupon(models.Model):
    name = models.CharField(max_length=250)
    coupon_code = models.CharField(max_length=250)
    incentive_type = models.CharField(max_length=250)
    incentive_value = models.DecimalField(max_digits=12, decimal_places=2)
    usage = models.CharField(max_length=250)
    start_datetime = models.DateTimeField('start date')
    end_datetime = models.DateTimeField('end date')
    is_exclusive = models.BooleanField()
    course = models.ManyToManyField(CourseOverview)
    associated_ecommerce_coupon_id = models.IntegerField()
    
    class Meta(object):
        app_label = "lhub_ecommerce_offer"
