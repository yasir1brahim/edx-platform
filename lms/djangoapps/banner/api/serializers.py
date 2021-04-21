"""
Serializers for Banner
"""
from rest_framework import serializers
from lms.djangoapps.banner.models import Banner
# from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
# class BannerRelatedSerializer(serializers.ModelSerializer):
#     """
#     Course Overview as single slung field
#     """
#     class Meta(object):
#         model = CourseOverview
#         fields = ('display_name')

class BannerSerializer(serializers.ModelSerializer):
    """
    Serializer for BadgeClass model.
    """
    course_over_view =  serializers.SlugRelatedField(
        read_only=True,
        slug_field='display_name'
     )
    class Meta(object):
        model = Banner
        fields = ('course_over_view', 'enabled', 'platform', 'slide_position', 'created_by', 'banner_img_url_txt')
