from rest_framework.generics import ListAPIView
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from openedx.core.lib.api.authentication import BearerAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from ..v1.models import Course
from ..v1.serializers import CourseSerializer

class CourseListView(ListAPIView):
    """ List courses and modes. """
    #authentication_classes = (JwtAuthentication, BearerAuthentication, SessionAuthentication,)
    #permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer
    pagination_class = None

    def get_queryset(self):
        return list(Course.iterator())
