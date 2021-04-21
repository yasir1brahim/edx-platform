"""
Signal related to banner

"""
from django.conf.urls.static import static
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.db.models import Signal
from .models import Banner
# from ecommerce.core.url_utils import get_lms_url

@receiver(post_save, sender=Banner)
def capture_image_url(sender, instance, created, **kwargs):
    if created:
        instance.banner_img_url_txt= str(instance.banner_img.url)
        instance.save()
    else:
        """prevent the loop back to post_save in case of update call
           pls refer this https://code.djangoproject.com/ticket/28970
        """
        Banner.objects.filter(pk=instance.id).update(banner_img_url_txt = str(instance.banner_img.url))





