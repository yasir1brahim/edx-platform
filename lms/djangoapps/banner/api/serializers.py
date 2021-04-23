"""
Serializers for Banner
"""
from rest_framework import serializers
from lms.djangoapps.banner.models import Banner
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from django.contrib.sites.shortcuts import get_current_site
from logging import getLogger
log = getLogger(__name__)

class BannerSerializer(serializers.ModelSerializer):
    """
    Serializer for BadgeClass model.
    """
    course_over_view =  serializers.SlugRelatedField(
        read_only=True,
        slug_field='display_name'
     )
    course_id = serializers.SerializerMethodField('course_id_')
    banner_img_url = serializers.SerializerMethodField('banner_img_url_')

    def course_id_(self, obj):
        if obj.course_over_view.display_name and obj.course_over_view.display_number_with_default:
            return str(CourseOverview.objects.filter(display_name = obj.course_over_view.display_name, display_number_with_default = obj.course_over_view.display_number_with_default).values_list('id', flat=True)[0])
        else:
            return None

    def banner_img_url_(self, obj):
        try:
            domain = str(get_current_site(request=None))
        except Exception as ex:
            log.error("Error while trying to fetch sites from Banner API " + str(ex))
        http = "http://"
        if http and domain and obj.banner_img_url_txt:
            return http+domain+str(obj.banner_img_url_txt)
        else:
            return str(obj.banner_img_url_txt)

    class Meta(object):
        model = Banner
        fields = ('course_id', 'course_over_view', 'enabled', 'platform', 'slide_position', 'created_by', 'banner_img_url')
