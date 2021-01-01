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
from student.models import CourseEnrollment

class CreateCourseReviewUser(APIView):
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)
    # Post request to create course review
    # Endpoint : /api/course_reviews/v2/create_course_review_user/

    def post(self,request):
        """
        """
        if ('course_id' in request.data) and ('rating' in request.data) and ('review' in request.data):
            if request.data['review'].strip():
                try:
                    checkFloat = float(request.data['rating'])
                    if CourseEnrollment.objects.filter(user=request.user, course_id=request.data['course_id']).exists():
                        course_data = CourseOverview.objects.filter(id=request.data['course_id'])
                        response = { "result":{}, "message": "Unknown error occured please try again later.", "status_code":500, "status":False  }
                        try:
                            review_object = CourseReviewModel.objects.create(user_id=request.user, course_id=course_data[0], rating=request.data['rating'], review=request.data['review'])
                            message = "Feedback submitted successfully."
                            response = { "result":{}, "message": message, "status_code":200, "status":True  }
                            return Response(response, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            message = "feedback already submitted."
                            response = { "result":{}, "message": message, "status_code":401, "status":False  }
                            return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        message = "user not enrolled."
                        response = { "result":{}, "message": message, "status_code":401, "status":False  }
                        return Response(response, status=status.HTTP_201_CREATED)
                except:
                    response = { "result":{}, "message": "Please provide a proper rating.", "status_code":401, "status":False  }
                    return Response(response, status=status.HTTP_201_CREATED)

            else:
                response = { "result":{}, "message": "Please provide a proper review.", "status_code":401, "status":False  }
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = { "result":{}, "message": "Missing one of the required field (course_id, rating, review).", "status_code":401, "status":False  }
            return Response(response, status=status.HTTP_201_CREATED)

