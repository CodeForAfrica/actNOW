from oauth2_provider.models import get_application_model
from rest_framework.permissions import BasePermission


class AllowAppicationsOnly(BasePermission):
    def has_permission(self, request, view):
        model = get_application_model()
        return model.objects.filter(user=request.user.id).exists()
