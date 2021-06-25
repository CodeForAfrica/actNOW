from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import OrganisationProfile, UserProfile
from .permissions import IsOrganisationMember, IsOwnerOrReadOnly
from .serializers import OrganisationProfileSerializer, UserProfileSerializer


class OrganisationProfileView(ModelViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = [IsAuthenticated, IsOrganisationMember]


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
