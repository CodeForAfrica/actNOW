from django.contrib.auth import get_user_model
from rest_framework import viewsets

from actnow.accounts.serializers import UserSerializer

from .permissions import AllowAppicationOwnerOnly, IsAuthenticated, IsOwnerOrReadOnly


class UsersView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = (AllowAppicationOwnerOnly,)
        else:
            permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        # Mark the user as in active instead of deleting them from DB
        instance.is_active = False
        # Revoke all OAuth tokens
        for access_token in instance.oauth2_provider_accesstoken.all():
            access_token.revoke()

        # Delete the DRF auth token
        instance.auth_token.delete()
        instance.save()
