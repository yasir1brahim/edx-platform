"""
CourseBlocks API views
"""


import six
from django.core.exceptions import ValidationError
from django.http import Http404
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from six import text_type

from openedx.core.lib.api.view_utils import DeveloperErrorViewMixin, view_auth_classes
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError

from .api import get_blocks
from .forms import BlockListGetForm
from opaque_keys.edx.keys import UsageKey
from lms.djangoapps.courseware.module_render import get_module_by_usage_id
from .views import BlocksView
from openedx.core.lib.api.authentication import (
    BearerAuthentication
)
from rest_framework.permissions import IsAuthenticated


class BlocksInCourseView(BlocksView):
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, hide_access_denials=False):  # pylint: disable=arguments-differ
        """
        Retrieves the usage_key for the requested course, and then returns the
        same information that would be returned by BlocksView.list, called with
        that usage key

        Arguments:
            request - Django request object
        """
        authentication_classes = (BearerAuthentication,)

        # convert the requested course_key to the course's root block's usage_key
        course_key_string = request.query_params.get('course_id', None)
        if not course_key_string:
            raise ValidationError('course_id is required.')

        try:
            course_key = CourseKey.from_string(course_key_string)
            course_usage_key = modulestore().make_course_usage_key(course_key)
            requested_params = request.query_params.copy()
            requested_params.update({'usage_key': course_usage_key, 'username': request.user.username})
            params = BlockListGetForm(requested_params, initial={'requesting_user': request.user})
            if not params.is_valid():
                raise ValidationError(params.errors)

            response = get_blocks(
                    request,
                    params.cleaned_data['usage_key'],
                    request.user,
                    params.cleaned_data['depth'],
                    params.cleaned_data.get('nav_depth'),
                    params.cleaned_data['requested_fields'],
                    params.cleaned_data.get('block_counts', []),
                    params.cleaned_data.get('student_view_data', []),
                    params.cleaned_data['return_type'],
                    params.cleaned_data.get('block_types_filter', None),
                    hide_access_denials=hide_access_denials,
                )
            for key,block in response['blocks'].items():
                if block['type'] == 'vertical':
                    usage_key = UsageKey.from_string(block['id'])
                    usage_key = usage_key.replace(course_key=modulestore().fill_in_run(usage_key.course_key))
                    course_key = usage_key.course_key
                    course = modulestore().get_course(course_key)
                    block_object, _ = get_module_by_usage_id(
                    request, text_type(course_key), text_type(usage_key), disable_staff_debug_info=True, course=course
                    )
                    completion_service = block_object.runtime.service(block_object, 'completion')
                    complete = completion_service.vertical_is_complete(block_object)
                    block.update({'is_completed': bool(complete)})

        except InvalidKeyError:
            raise ValidationError(u"'{}' is not a valid course key.".format(six.text_type(course_key_string)))
        return Response(response)

