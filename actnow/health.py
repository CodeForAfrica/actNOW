from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .petitions.models import Petition


@api_view(["GET"])
def health_check(request):
    try:
        Petition.objects.count()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
