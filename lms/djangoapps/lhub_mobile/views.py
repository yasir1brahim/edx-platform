from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions
from .models import MobileUserSessionCookie

class UserSessionCookieView(ViewSet):
    """
        **Use Cases**

            Get  a user's session cookie for mobile apps webview.

        **Example Request**

            GET /api/lhub_mobile/getSessionCookie/

    """
    authentication_classes = (
        BearerAuthenticationAllowInactiveUser, SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        session_cookies = MobileUserSessionCookie.objects.filter(user=request.user)
        if session_cookies:
            session_cookie_obj = session_cookies.latest('id')
            return Response({'message': "", 'status': True, 'result':{'session_cookie': session_cookie_obj.session_cookie}, 'status_code':200})
        return Response({'message': "Session Cookie Not Found", 'status': True, 'result':{}, 'status_code':400})


