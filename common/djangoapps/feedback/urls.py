from django.conf import settings
from django.conf.urls import url
from .mobile_views import ReviewListView
from .views import CreateCourseReviewUser

urlpatterns = [
    url(r'^v2/create_course_review_user/', CreateCourseReviewUser.as_view()),
    url(r'^v2/courses/{}'.format(settings.COURSE_KEY_PATTERN), ReviewListView.as_view(), name="review-list"),
]
