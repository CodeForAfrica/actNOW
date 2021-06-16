from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from actnow.accounts.serializers import UserRegistrationSerializer

from .permissions import AllowAppicationsOnly
from .utils import email_address_exists, username_exists


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAppicationsOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if email_address_exists(serializer.data["email"]):
            response = _("A user is already registered with this e-mail address.")
            response_status = status.HTTP_400_BAD_REQUEST
            return Response({"error": response}, status=response_status)

        if username_exists(serializer.data["username"]):
            response = _("A user is already registered with this username")
            response_status = status.HTTP_400_BAD_REQUEST
            return Response({"error": response}, status=response_status)

        serializer.save(self.request)

        return Response(
            status=status.HTTP_201_CREATED,
        )
