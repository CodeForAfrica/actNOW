from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from actnow.accounts.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(self.request)
        token = Token.objects.create(user=user)

        return Response(
            {"token": token.key},
            status=status.HTTP_201_CREATED,
        )
