from rest_framework.generics import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import OrganisationProfile, Profile, UserProfile
from .permissions import IsOrganisationOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    OrganisationProfileSerializer,
    ProfileSerializer,
    UserProfileSerializer,
)


class ProfileView(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class OrganisationProfileView(ModelViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = [IsAuthenticated, IsOrganisationOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            owners=[
                self.request.user,
            ]
        )


class UserProfileView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
