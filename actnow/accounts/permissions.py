from oauth2_provider.models import get_id_token_model
from rest_framework.permissions import BasePermission


class AllowAppicationsOnly(BasePermission):
    def has_permission(self, request, view):
        application_id_token = request.data.get("application_token")
        jti = get_id_token_model().objects.filter(jti__iexact=application_id_token)
        if not jti.exists():
            return False
        return jti.first().is_valid()
