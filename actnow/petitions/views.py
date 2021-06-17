from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer


class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SignatureView(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Signature.objects.filter(signatory=self.request.user)
