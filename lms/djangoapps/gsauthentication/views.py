
from openedx.core.djangoapps.oauth_dispatch.views import AccessTokenView
from oauth2_provider.models import AccessToken as Token
from rest_framework.response import Response
import logging
from rest_framework.views import APIView
from django.contrib.auth.models import User
import requests
import json 
from django.conf import settings

def get_response(
    message='',
    result={},
    status=False,
    status_code=200
    ):
    return {
        'message': message,
        'result': result,
        'status': status,
        'status_code': status_code
    }



class CustomObtainAuthToken(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = dict(request.POST.lists())
            undata = {}
            for key, value in data.items():
                undata[key] = value[0]
            
            if not request.POST.get("token_type"):
                return Response({"status":"false","status_code":400,"result":{},"message": "Missing data token_type."})

            user_exist = User.objects.filter(email=request.POST.get("username")).exists()
            if user_exist:
                user = User.objects.get(email=request.POST.get("username"))
            else:
                user = User.objects.get(username=request.POST.get("username"))

            if user.check_password(request.POST.get("password")):
                if user.is_active:
                    response = requests.post(settings.LMS_ROOT_URL+"/oauth2/access_token", data=undata)
                    resp_json = {}
                    response_json = response.json()
                    if "error" in response_json:
                        resp_json['message'] = response_json['error']
                        resp_json['status_code']=400
                        resp_json['result']={}
                        resp_json['status']="false"
                    if "access_token" in response_json:
                        response_json['username'] = user.username
                        resp_json['result'] = response_json
                        resp_json['message'] = "Success"
                        resp_json['status_code']=200
                        resp_json['status']="true"
                    return Response(resp_json)
                else:
                    return Response({"status":"false","status_code":400,"result":{},"message": "Email not verified."})
            else:
                return Response({"status":"false","status_code":400,"result":{},"message": "Invalid username or password."})

        except Exception as e:
                return Response({"status":"false","status_code":400,"result":{},"message": str(e)})
