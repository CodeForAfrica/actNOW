from rest_framework.generics import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import OrganisationProfile, UserProfile
from .permissions import IsOrganisationOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import OrganisationProfileSerializer, UserProfileSerializer


class OrganisationProfileView(ModelViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = [IsAuthenticated, IsOrganisationOwnerOrReadOnly]


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
