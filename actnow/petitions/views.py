from rest_framework import mixins, viewsets

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer


class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer


class SignatureView(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer

    def get_queryset(self):
        return Signature.objects.filter(signatory=self.request.user)
