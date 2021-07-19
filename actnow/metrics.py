from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from actnow.petitions.models import Petition, Signature
from actnow.petitions.serializers import PetitionSerializer

User = get_user_model()


@api_view(["GET"])
def metrics(request):
    return Response(
        {
            "metrics": {
                "users": {
                    "count": User.objects.count(),
                },
                "petitions": {
                    "count": Petition.objects.count(),
                },
                "signatures": {
                    "count": Signature.objects.count(),
                },
                "latestPetitions": {
                    "count": 5,
                    "items": PetitionSerializer(
                        Petition.objects.order_by("-created_at")[:5], many=True
                    ).data,
                },
            }
        }
    )
