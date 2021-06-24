from oauth2_provider.models import get_application_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowAppicationOwnerOnly(BasePermission):
    def has_permission(self, request, view):
        Application = get_application_model()
        return Application.objects.filter(user=request.user.id).exists()


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return bool(obj.id == request.user.id)


class IsNotDeleted(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not request.user.is_deleted
        )
