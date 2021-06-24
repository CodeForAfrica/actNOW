from django.contrib.auth import get_user_model
from rest_framework import viewsets

from actnow.accounts.serializers import UserSerializer

from .permissions import AllowAppicationOwnerOnly, IsNotDeleted, IsOwnerOrReadOnly


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_deleted=False)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                AllowAppicationOwnerOnly,
            ]
        else:
            permission_classes = [IsOwnerOrReadOnly, IsNotDeleted]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        # Mark the user account as deleted instead of deleting it from the DB
        instance.is_deleted = True
        instance.is_active = False
        # Revoke all OAuth tokens
        for access_token in instance.oauth2_provider_accesstoken.all():
            access_token.revoke()

        # Delete the DRF auth token
        instance.auth_token.delete()
        instance.save()
