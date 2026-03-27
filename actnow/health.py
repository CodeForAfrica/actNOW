from django.db import OperationalError, connections
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """Meta view to check the status of core services."""
    data = {"status": "healthy", "detail": "server and core services available"}
    try:
        connections["default"].cursor()
    except OperationalError:
        data["status"] = "unhealthy"
        data["detail"] = "unable to connect to database server"
        return Response(data=data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data=data, status=status.HTTP_200_OK)
