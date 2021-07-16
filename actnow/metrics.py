from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from actnow.petitions.models import Petition

User = get_user_model()


@api_view(["GET"])
def metrics(request):
    return Response(
        {
            "metrics": {
                "users": {
                    "total": User.objects.count(),
                },
                "petitions": {
                    "total": Petition.objects.count(),
                },
            }
        }
    )
