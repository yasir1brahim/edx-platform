from rest_framework.generics import ListAPIView
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from openedx.core.lib.api.authentication import BearerAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .filters import LazyPageNumberPagination

from ..v1.models import Course
from ..v1.serializers import CourseSerializer

class CourseListView(ListAPIView):
    """ List courses and modes. """
    class CourseListPageNumberPagination(LazyPageNumberPagination):
        max_page_size = 100
    #authentication_classes = (JwtAuthentication, BearerAuthentication, SessionAuthentication,)
    #permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer
    pagination_class = CourseListPageNumberPagination

    def get_queryset(self):
        return list(Course.iterator())
