from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from actnow.profiles.models import OrganisationProfile, Profile, UserProfile

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer


class PetitionView(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    filterset_fields = ["owner", "followers"]

    def perform_create(self, serializer):
        organisation = self.request.GET.get("organisation")
        if organisation:
            owner = OrganisationProfile.objects.get(pk=organisation)
            # TODO(kilemensi): Check if self.request.user is one of organisation owners
        else:
            user_profile = UserProfile.objects.get(user=self.request.user)
            owner = Profile.objects.get(user_profile=user_profile)

        serializer.save(owner=owner)


class SignatureView(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer

    def get_queryset(self):
        signatory = self.request.GET.get("signatory")
        if signatory:
            # TODO(kilemensi): Check if signatory is user_profile
            #                  or organisation profile
            return Signature.objects.filter(signatory=signatory)

        return Signature.objects.all()

    def perform_create(self, serializer):
        serializer.save(signatory=self.request.user)


@api_view(["GET", "POST"])
@authentication_classes(
    [SessionAuthentication, TokenAuthentication, OAuth2Authentication]
)
@permission_classes([IsAuthenticated])
def follow_petition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    if request.method == "POST":
        petition.followers.add(request.user)
        petition.save()
    petition_serializer = PetitionSerializer(petition)
    return Response(data=petition_serializer.data)
