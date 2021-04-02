from json import encoder
import json
from django.db.models.fields.files import ImageFieldFile
from django.http.response import JsonResponse
from openedx.core.lib.api.permissions import ApiKeyHeaderPermission
from os import name
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import FaqCategoryIDSerializer, FaqCategoryTopSerializer, FaqDetailsSerializer, FaqSerializer, FaqCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Faq, FaqCategory
from .models import Faq

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from openedx.core.lib.api.authentication import BearerAuthentication
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer

class FaqCategoryViewSet(viewsets.ModelViewSet):
    queryset = FaqCategory.objects.all()
    serializer_class = FaqCategorySerializer


# class ApiKeyPermissionMixIn(object):
#     """
#     This mixin is used to provide a convenience function for doing individual permission checks
#     for the presence of API keys.
#     """

#     def has_api_key_permissions(self, request):
#         """
#         Checks to see if the request was made by a server with an API key.

#         Args:
#             request (Request): the request being made into the view

#         Return:
#             True if the request has been made with a valid API key
#             False otherwise
#         """
#         return ApiKeyHeaderPermission().has_permission(request, self)

class FaqDetailsView(generics.RetrieveAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqDetailsSerializer
    authentication_classes = (JwtAuthentication, BearerAuthentication)
    permission_classes = (IsAuthenticated, )    

    def get(self, request, pk):
        try:
            faq = Faq.objects.get(id=pk)
            faq.view_count = faq.view_count + 1
            faq.save(update_fields=("view_count",))
        except Faq.DoesNotExist:
            return Response({'error': 'Not found.', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        detail_serailizer = FaqDetailsSerializer(faq)
        return Response({"result": detail_serailizer.data, "status_code": status.HTTP_200_OK, "message": "FAQ Details.", "status": True}, status=status.HTTP_200_OK)

class FaqCategoryIDView(generics.ListAPIView):
    authentication_classes = (JwtAuthentication, BearerAuthentication)
    permission_classes = (IsAuthenticated, )
    queryset = Faq.objects.all()
    serializer_class = FaqCategoryIDSerializer

    def get(self, request, category_id):
        try:
            faq = Faq.objects.filter(category_id=category_id)
            results = [ob.as_json() for ob in faq]
        except Faq.DoesNotExist:
            return Response({'error': 'Not found.', 'status_code': status.HTTP_400_BAD_REQUEST, "status": False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': results, 'status_code': status.HTTP_200_OK, 'message': 'FAQ the list of questions of a category.', 'status': True}, status=status.HTTP_200_OK)

# class ExtendedEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ImageFieldFile):
#             return str(obj)
#         else:
#             return super().default(obj)

class FaqTopCategoryView(generics.RetrieveAPIView):
    authentication_classes = (JwtAuthentication, BearerAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            faq_category = FaqCategory.objects.all()
            category_serializer = FaqCategoryTopSerializer(faq_category, many=True, context={"request": request})
            faq = Faq.objects.all().order_by('-view_count')[:10]
            faq_json = [ob.as_json() for ob in faq]
        except:
            return Response({'error': "Not Found", 'status_code': status.HTTP_400_BAD_REQUEST, 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': {'categories': category_serializer.data, 'top': faq_json}, 'status_code': status.HTTP_200_OK, 'message': 'FAQ Top Category.', 'status': True}, status=status.HTTP_200_OK)
