from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from openedx.core.lib.api.authentication import BearerAuthentication
from common.djangoapps.edxmako.shortcuts import render_to_response

from lms.djangoapps.lhub_notification.models import Notification
from lms.djangoapps.lhub_notification.serializers import NotificationSerializer


class NotificationViewSet(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (JwtAuthentication, BearerAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            is_delete=False
        )

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class NotificationListView(ListView):
    paginate_by = 10
    context_object_name = 'notification_list'
    template_name = 'lhub_notification/notification_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            is_delete=False
        )

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return render_to_response(self.template_name, context)


class NotificationDetail(DetailView):
    context_object_name = 'notification'
    template_name = 'lhub_notification/notification_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            is_delete=False
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_read = True
        self.object.save()
        context = self.get_context_data(object=self.object)
        return render_to_response(self.template_name, context)
