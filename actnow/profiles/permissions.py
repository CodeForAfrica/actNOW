from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.user.id == request.user.id)


class IsUserProfile(BasePermission):
    def has_permission(self, request, view):
        user_id = request.data.get("user", -1)
        # Prevent a user from creating other users profiles.
        return int(user_id) == request.user.id
