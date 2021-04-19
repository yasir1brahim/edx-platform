from django.db.models import Avg
from django.db import IntegrityError
from django.template.loader import render_to_string
from web_fragments.views import FragmentView
from web_fragments.fragment import Fragment
from opaque_keys.edx.keys import CourseKey
from lms.djangoapps.courseware.courses import get_course_with_access, get_course_overview_with_access
from common.djangoapps.feedback.models import CourseReview
from collections import OrderedDict
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


class ReviewsTabFragmentView(FragmentView):
    """
    Fragment view implementation of the reviews tab.
    """
    def render_to_fragment(self, request, course_id=None, **kwargs):
        """
        Render the reviews tab to a fragment.
        Args:
            request: The Django request.
            course_id: The id of the course.
        Returns:
            Fragment: The fragment representing the reviews tab.
        """
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)
        reviews = CourseReview.objects.filter(course_id=course_id)
        average_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0.00, 2)
        is_commented = CourseReview.objects.filter(course_id=course_id, user_id=request.user).exists()
        num_reviews = reviews.count()
        rating_percent_dict = OrderedDict()

        for index in range(1, 6):
            rating_type_value = reviews.filter(rating=index).count()

            try:
                percent = round(rating_type_value * 100 / num_reviews, 2)
            except ZeroDivisionError:
                percent = 0

            rating_percent_dict.update({index: percent})

        context = {
            'course': course,
            'user': request.user,
            'reviews': reviews,
            'average_rating': average_rating,
            'create_review_url': reverse("create_review", kwargs={"course_id": course_id}),
            'is_commented': is_commented,
            'rating_percent_dict': rating_percent_dict
        }
        html = render_to_string('reviews/reviews.html', context)
        fragment = Fragment(html)
        fragment.add_javascript_url(staticfiles_storage.url('reviews/js/reviews.js'))
        fragment.add_javascript_url(staticfiles_storage.url('reviews/js/jquery.rateit.min.js'))
        fragment.add_css_url(staticfiles_storage.url('reviews/css/rateit.css'))
        fragment.add_css_url(staticfiles_storage.url('reviews/css/star.gif'))
        fragment.add_css_url(staticfiles_storage.url('reviews/css/delete.gif'))

        return fragment


@login_required
@require_http_methods(['POST'])
def create_review(request, course_id):
    rating = request.POST.get('rating')
    review = request.POST.get('review')
    course_key = CourseKey.from_string(course_id)
    course = get_course_overview_with_access(request.user, "load", course_key)

    try:
        rating = float(rating)
    except (TypeError, ValueError):
        return JsonResponse({'message': 'Set the rating'}, status=400)

    if not rating:
        return JsonResponse({'message': 'Set the rating'}, status=400)

    if not review:
        return JsonResponse({'message': 'Give a review'}, status=400)

    try:
        CourseReview.objects.create(
            user_id=request.user,
            course_id=course,
            rating=rating,
            review=review
        )
    except IntegrityError:
        return JsonResponse({'message': 'Review is already existed'}, status=400)

    return JsonResponse({'message': 'Success'}, status=200)



