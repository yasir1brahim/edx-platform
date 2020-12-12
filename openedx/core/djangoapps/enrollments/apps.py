
"""
Enrollments Application Configuration

Signal handlers are connected here.
"""


from django.apps import AppConfig
from django.conf import settings
from edx_django_utils.plugins import PluginSettings
from edx_proctoring.runtime import set_runtime_service

from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType


class EnrollmentsConfig(AppConfig):
    """
    Application Configuration for Enrollments.
    """
    name = u'openedx.core.djangoapps.enrollments'

    def ready(self):
        """
        Connect handlers to fetch enrollments.
        """
        if settings.FEATURES.get('ENABLE_SPECIAL_EXAMS'):
            from .services import EnrollmentsService
            set_runtime_service('enrollments', EnrollmentsService())
