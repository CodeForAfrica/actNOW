from rest_framework.permissions import BasePermission


class ActNowCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user.is_staff)

        return bool(request.user.is_authenticated)
