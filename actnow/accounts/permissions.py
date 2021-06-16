from oauth2_provider.models import get_application_model
from rest_framework.permissions import BasePermission


class AllowAppicationOwnerOnly(BasePermission):
    def has_permission(self, request, view):
        Application = get_application_model()
        return Application.objects.filter(user=request.user.id).exists()
