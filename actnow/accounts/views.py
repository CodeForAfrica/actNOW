from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response

from actnow.accounts.serializers import UserSerializer
from actnow.profiles.serializers import UserProfileSerializer

from .permissions import AllowAppicationOwnerOnly, IsNotDeleted, IsOwnerOrReadOnly


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user_account_serializer = self.get_serializer(data=request.data)
        user_account_serializer.is_valid(raise_exception=True)
        user_account = self.perform_create(user_account_serializer)

        user_profile_data = {
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", ""),
            "location": request.data.get("location", ""),
            "photo": request.data.get("photo", ""),
            "social_media_link": request.data.get("social_media_link", ""),
            "user": user_account.id,
        }
        user_profile_serializer = UserProfileSerializer(data=user_profile_data)
        if not user_profile_serializer.is_valid():
            # Delete the user account too
            user_account.delete()
            return Response(
                user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(user_profile_serializer)
        headers = self.get_success_headers(user_profile_serializer.data)
        return Response(
            user_profile_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

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

    def perform_create(self, serializer):
        return serializer.save()

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
