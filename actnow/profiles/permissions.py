from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user.is_authenticated)
        return request.user.id in obj.persons.values_list("id", flat=True)
