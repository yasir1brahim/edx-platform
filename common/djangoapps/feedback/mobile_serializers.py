"""
Course Review API Serializers.
"""


import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request
from django.urls import reverse
from rest_framework import serializers

from openedx.core.lib.api.fields import AbsoluteURLField


class ReviewSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Course Review objects providing minimal data about the course.
    
    """

    created_at = serializers.DateField()
    id = serializers.CharField()  # pylint: disable=invalid-name
    review = serializers.CharField()
    rating = serializers.CharField()
    course_id_id = serializers.CharField()
    user_id_id = serializers.CharField()

    def get_hidden(self, course_overview):
        """
        Get the representation for SerializerMethodField `hidden`
        Represents whether course is hidden in LMS
        """
        catalog_visibility = course_overview.catalog_visibility
        return catalog_visibility in ['about', 'none']

    def get_blocks_url(self, course_overview):
        """
        Get the representation for SerializerMethodField `blocks_url`
        """
        base_url = '?'.join([
            reverse('blocks_in_course'),
            six.moves.urllib.parse.urlencode({'course_id': course_overview.id}),
        ])
        return self.context['request'].build_absolute_uri(base_url)

