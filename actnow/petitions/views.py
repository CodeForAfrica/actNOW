from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Petition
from .serializers import PetitionSerializer


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
