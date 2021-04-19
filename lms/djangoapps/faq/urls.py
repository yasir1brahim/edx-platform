from os import name
from django.db import models, router
from rest_framework import routers, urlpatterns
from django.conf.urls import include, url
from django.urls import path
from .views import FaqCategoryIDView, FaqTopCategoryView, FaqViewSet, FaqCategoryViewSet, FaqDetailsView
from .models import Faq
from .utils import CustomReadOnlyRouter
from django.conf import settings
from django.conf.urls.static import static

router = CustomReadOnlyRouter()
router.register(r'faq', FaqViewSet, basename='faq_api')
router.register(r'faq_category', FaqCategoryViewSet, basename='faq_category_api')

urlpatterns = [
    url(r'^category_top/$', FaqTopCategoryView.as_view(), name='category_top'),
    url(r'^v0/', include((router.urls, 'faq_api'), namespace='v0')),
]

urlpatterns += [
    path(r'category/<str:category_id>/', FaqCategoryIDView.as_view()),
]


urlpatterns += [
    url(r'^question/(?P<pk>\d+)$', FaqDetailsView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
