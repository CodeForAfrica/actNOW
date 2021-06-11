from oauth2_provider.models import get_application_model
from rest_framework.permissions import BasePermission


class ActNowCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user.is_staff)

        return bool(request.user.is_authenticated)


class AllowOnlyApplicationToRegisterNewUser(BasePermission):
    def has_permission(self, request, view):
        app_client_id = request.data.get("app_client_id")
        return get_application_model().objects.filter(client_id=app_client_id).exists()
