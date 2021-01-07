from openedx.core.djangoapps.oauth_dispatch.views import AccessTokenView
from oauth2_provider.models import AccessToken as Token
from rest_framework.response import Response
import logging
from rest_framework.views import APIView
from django.contrib.auth.models import User
import requests
import json 
from django.conf import settings

class CustomObtainAuthToken(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user_exist = User.objects.filter(email=request.POST.get("username")).exists()
            if user_exist:
                user = User.objects.get(email=request.POST.get("username"))
            else:
                user = User.objects.get(username=request.POST.get("username"))
            if user.is_active:
                response = requests.post(settings.LMS_ROOT_URL+"/oauth2/access_token", params=request.POST)
                resp_json = response.json()
                if "access_token" in resp_json:
                    resp_json['username'] = user.username
                return Response(resp_json)
            else:
                return Response({"error": "Email not verified."})
        except:
                return Response({"error": "Invalid username."})
