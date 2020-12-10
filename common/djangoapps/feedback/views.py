from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CourseReview as CourseReviewModel
from rest_framework.response import Response
from rest_framework import status
from openedx.core.lib.api.view_utils import view_auth_classes
from django.utils.functional import SimpleLazyObject
from django.core.exceptions import ObjectDoesNotExist
from lms.djangoapps.mobile_api.decorators import mobile_view
import logging
from .serializers import CourseReviewSerializer
from django.contrib.auth.decorators import login_required
log = logging.getLogger(__name__)
from rest_framework import mixins
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from util.db import outer_atomic
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from openedx.core.lib.api.authentication import BearerAuthentication
from django.contrib.auth.models import User
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

class CreateCourseReviewUser(APIView):
    authentication_classes = (BearerAuthentication,)

    def post(self,request):
        """
        """
        user_data = User.objects.filter(id=70)
        course_data = CourseOverview.objects.filter(id=request.data['course_id'])
        review_object = CourseReviewModel.objects.create(user_id=request.user, course_id=course_data[0], rating=request.data['rating'], review=request.data['review'])
        response = "success" 
        return Response(response, status=status.HTTP_201_CREATED)


