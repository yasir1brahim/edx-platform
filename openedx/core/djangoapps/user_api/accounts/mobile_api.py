from .api import update_account_settings, get_account_extra_settings
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions,status
from openedx.core.lib.api.parsers import MergePatchParser
from rest_framework.response import Response
from django.db import transaction
from rest_framework.viewsets import ViewSet
import logging
from ..errors import AccountUpdateError, AccountValidationError, UserNotAuthorized, UserNotFound
import datetime

class AccountViewSet(ViewSet):

    authentication_classes = (
        BearerAuthenticationAllowInactiveUser, SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MergePatchParser,)

    def retrieve(self, request, username):
        """
        GET /api/user/v1/accounts/{username}/
        """
        try:
            account_settings = get_account_extra_settings(
                request, [username], view=request.query_params.get('view'))
            if account_settings[0]['date_of_birth']:
                account_settings[0]['age'] = datetime.date.today().year - account_settings[0]['date_of_birth'].year
        except UserNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(account_settings[0])

    def partial_update(self, request, username):
        """
        PATCH /api/user/v1/accounts/{username}/

        Note that this implementation is the "merge patch" implementation proposed in
        https://tools.ietf.org/html/rfc7396. The content_type must be "application/merge-patch+json" or
        else an error response with status code 415 will be returned.
        """
        try:
            with transaction.atomic():
                update_account_settings(request.user, request.data, username=username)
                account_settings = get_account_extra_settings(request, [username])[0]
                if account_settings['date_of_birth']:
                    account_settings['age'] = datetime.date.today().year - account_settings['date_of_birth'].year
        except UserNotAuthorized:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except UserNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except AccountValidationError as err:
            return Response({"field_errors": err.field_errors}, status=status.HTTP_400_BAD_REQUEST)
        except AccountUpdateError as err:
            return Response(
                {
                    "developer_message": err.developer_message,
                    "user_message": err.user_message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(account_settings)
