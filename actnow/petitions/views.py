from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import PetitionSerializer, PetitiionSignatorSerializer
from .models import Petition, PetitionSignator

class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer

class PetitionSignatorView(generics.ListCreateAPIView):
    queryset = PetitionSignator.objects.all()
    serializer_class = PetitionSerializer