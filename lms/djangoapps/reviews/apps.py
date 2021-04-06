from django.apps import AppConfig
from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.constants import COURSE_ID_PATTERN
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType


class ReviewsConfig(AppConfig):
    name = 'lms.djangoapps.reviews'
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: u'',
                PluginURLs.REGEX: u'^courses/{}/reviews/'.format(COURSE_ID_PATTERN),
                PluginURLs.RELATIVE_PATH: u'urls',
            }
        }
    }
