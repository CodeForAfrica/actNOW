from oauth2_provider.models import get_id_token_model
from rest_framework.permissions import BasePermission


class ActNowCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user.is_staff)

        return bool(request.user.is_authenticated)


class AllowOnlyApplicationToRegisterNewUser(BasePermission):
    def has_permission(self, request, view):
        application_id_token = request.data.get("id_token")
        id_token = get_id_token_model().objects.filter(jti__iexact=application_id_token)
        if not id_token.exists():
            return False
        return id_token.first().is_valid()
