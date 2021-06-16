from rest_framework import viewsets
from rest_framework import generics
from .serializers import PetitionSerializer, PetitionSignatureSerializer
from .models import Petition, PetitionSignature

class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer

class PetitionSignatureView(generics.ListCreateAPIView):
    queryset = PetitionSignature.objects.all()
    serializer_class = PetitionSignatureSerializer