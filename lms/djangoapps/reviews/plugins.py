"""
Definition of the course review feature.
"""

from django.utils.translation import ugettext_noop
from lms.djangoapps.courseware.tabs import EnrolledTab
from xmodule.tabs import TabFragmentViewMixin
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class ReviewsTab(TabFragmentViewMixin, EnrolledTab):
    """
    The representation of the course reviews view type.
    """
    name = "reviews"
    tab_id = "reviews"

    type = "reviews"
    title = ugettext_noop("Reviews")
    body_class = "reviews-tab"
    is_hideable = False
    is_default = True
    fragment_view_name = 'lms.djangoapps.reviews.views.ReviewsTabFragmentView'

    @classmethod
    def is_enabled(cls, course, user=None):
        """Returns true if the reviews feature is enabled in the course.

        Args:
            course (CourseDescriptor): the course using the feature
            user (User): the user interacting with the course
        """
        if not super(ReviewsTab, cls).is_enabled(course, user=user):
            return False

        course = CourseOverview.get_from_id(course.id)
        return course.allow_review
