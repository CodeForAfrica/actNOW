from rest_framework.generics import ListCreateAPIView

from actnow.profiles.models import UserProfile
from actnow.profiles.permissions import ActNowCreatePermission
from actnow.profiles.serializers import UserProfileSerializer


class UserProfileView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        ActNowCreatePermission,
    ]
