from rest_framework import viewsets

from actnow.profiles.models import OrganisationProfile, Profile, UserProfile

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer


def get_profile(request):
    organisation = request.GET.get("organisation")
    if organisation:
        # TODO(kilemensi): Check if self.request.user is one of organisation owners
        return OrganisationProfile.objects.get(pk=organisation)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        return Profile.objects.get(user_profile=user_profile)


class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    filterset_fields = ["owner", "followers", "signatures"]

    def perform_create(self, serializer):
        owner = get_profile(self.request)
        serializer.save(owner=owner)


class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer

    def get_queryset(self):
        signatory = self.request.GET.get("signatory")
        if signatory:
            # TODO(kilemensi): Check if signatory is either user
            #                  or organisation profile
            return Signature.objects.filter(signatory=signatory)

        return Signature.objects.all()

    def perform_create(self, serializer):
        signatory = get_profile(self.request)
        serializer.save(signatory=signatory)
