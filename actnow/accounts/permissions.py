from oauth2_provider.models import Application
from rest_framework.permissions import BasePermission


class AllowAppicationsOnly(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Application)
