from rest_framework.generics import ListAPIView
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from openedx.core.lib.api.authentication import BearerAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .filters import LazyPageNumberPagination
from operator import attrgetter
from ..v1.models import Course
from ..v1.serializers import CourseSerializer
import logging
log = logging.getLogger(__name__)
import json
class CourseListView(ListAPIView):
    """ List courses and modes. """
    class CourseListPageNumberPagination(LazyPageNumberPagination):
        max_page_size = 100
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer
    pagination_class = CourseListPageNumberPagination
    # filter_class = CourseListFilter
    # filterset_class = CourseListFilter
    # filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        filtered_courses = []
        filter = False
        filters = {'difficulty_level': None, 'sale_type': None, 'subcategory_id': None,'discount_applicable': None, 'is_premium': 'Boolean'}
        request_filters = {}
        for f,val in filters.items():
            filter_val = self.request.query_params.get(f, None)
            if filter_val is not None:
                filter = True
                if val == 'Boolean':
                    boolean_result = [json.loads(filter_val.split(',')[0].lower())]
                    request_filters[f] = boolean_result
                else:
                    request_filters[f] = filter_val.split(',')
        courses = list(Course.iterator(self.request.META.get('HTTP_AUTHORIZATION', None)))
        ordering_filter=self.request.query_params.get('ordering', None)
        if ordering_filter:
            ordering_filter_list = ordering_filter.split(',')
            courses = self.order_courses(courses, ordering_filter_list)
        if filter:
            for course in courses:
                is_filter = [True if getattr(course,f) in val and val is not None else False for f,val in request_filters.items()]
                if all(is_filter):
                    filtered_courses.append(course)
        else:
            return courses
        return filtered_courses

    def order_courses(self,course_list, ordering):
        allowed_ordering = ["ratings", "-ratings", "enrollments_count", "-enrollments_count", "created", "-created", "discounted_price", "-discounted_price"]
        
        for order in ordering:
            if order in allowed_ordering:
                if order == "-ratings":
                   course_list.sort(key=lambda x: (x.ratings is None, x.ratings), reverse=True)
                elif order == "ratings":
                    course_list.sort(key=lambda x: (x.ratings is None, x.ratings))
                if order == "-enrollments_count":
                   course_list.sort(key=lambda x: (x.enrollments_count is None, x.enrollments_count), reverse=True)
                elif order == "enrollments_count":
                    course_list.sort(key=lambda x: (x.enrollments_count is None, x.enrollments_count))
                if order == "-created":
                   course_list.sort(key=lambda x: (x.created is None, x.created), reverse=True)
                elif order == "created":
                    course_list.sort(key=lambda x: (x.created is None, x.created))
                if order == "-discounted_price":
                   course_list.sort(key=lambda x: (x.discounted_price is None, x.discounted_price), reverse=True)
                elif order == "discounted_price":
                    course_list.sort(key=lambda x: (x.discounted_price is None, x.discounted_price))

        return course_list
