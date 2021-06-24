from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import OrganisationProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import OrganisationProfileSerializer


class OrganisationProfileView(ModelViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
