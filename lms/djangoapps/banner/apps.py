"""
App Configuration
"""
from django.apps import AppConfig

class BannerConfig(AppConfig):
    name = 'lms.djangoapps.banner'
    verbose_name = 'banner'

    def ready(self):
        super().ready()
        # noinspection PyUnresolvedReferences
        import lms.djangoapps.banner.signals
