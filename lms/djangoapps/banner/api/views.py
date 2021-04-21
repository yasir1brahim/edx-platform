"""
API views for banner
"""

from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import generics
from rest_framework.exceptions import APIException
from lms.djangoapps.banner.models import Banner
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from .serializers import BannerSerializer

class BannerApi(generics.ListAPIView):
    serializer_class = BannerSerializer
    authentication_classes = (
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser
    )

    def get_queryset(self):
        """
        The query will return 1 to 10 images of banner, platform is both(mobile, web) or mobile alone as of now
        """
        queryset = Banner.objects.filter(slide_position__gte=1, slide_position__lte=10, platform__in = ['MOBILE', 'BOTH'])
        return queryset
