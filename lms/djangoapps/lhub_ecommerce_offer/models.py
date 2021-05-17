from django.db import models
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

# Create your models here.

class Offer(models.Model):
    incentive_type = models.CharField(max_length=250)
    incentive_value = models.DecimalField(max_digits=12, decimal_places=2)
    condition_type = models.CharField(max_length=250)
    condition_value = models.DecimalField(max_digits=12, decimal_places=2)
    start_datetime = models.DateTimeField('date published')
    end_datetime = models.DateTimeField('date published')
    priority = models.IntegerField()
    is_exclusive = models.BooleanField()
    associated_ecommerce_offer_id = models.IntegerField()
    course = models.ManyToManyField(CourseOverview)
    is_active = models.BooleanField()
    
    class Meta(object):
        app_label = "lhub_ecommerce_offer"
        