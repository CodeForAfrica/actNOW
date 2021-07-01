from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.user.id == request.user.id)


class IsOrganisationMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.id in obj.persons.values_list("id", flat=True)


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False
