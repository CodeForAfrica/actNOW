from rest_framework import mixins, permissions, viewsets

from .models import Petition, PetitionSignature
from .serializers import PetitionSerializer, PetitionSignatureSerializer


class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PetitionSignatureView(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = PetitionSignature.objects.all()
    serializer_class = PetitionSignatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PetitionSignature.objects.filter(signator = self.request.user) 
