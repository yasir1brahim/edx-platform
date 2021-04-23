"""
Serializers for Banner
"""
from rest_framework import serializers
from lms.djangoapps.banner.models import Banner
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class BannerSerializer(serializers.ModelSerializer):
    """
    Serializer for BadgeClass model.
    """
    course_over_view =  serializers.SlugRelatedField(
        read_only=True,
        slug_field='display_name'
     )
    course_id_ = serializers.SerializerMethodField('course_id')

    def course_id(self, obj):
        if obj.course_over_view.display_name and obj.course_over_view.display_number_with_default:
            return str(CourseOverview.objects.filter(display_name = obj.course_over_view.display_name, display_number_with_default = obj.course_over_view.display_number_with_default).values_list('id', flat=True)[0])
        else:
            return None

    class Meta(object):
        model = Banner
        fields = ('course_id_', 'course_over_view', 'enabled', 'platform', 'slide_position', 'created_by', 'banner_img_url_txt')
