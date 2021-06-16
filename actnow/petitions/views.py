from rest_framework import generics, permissions, viewsets

from .models import Petition, PetitionSignature
from .serializers import PetitionSerializer, PetitionSignatureSerializer


class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer


class PetitionSignatureView(generics.ListCreateAPIView):
    queryset = PetitionSignature.objects.all()
    serializer_class = PetitionSerializer
