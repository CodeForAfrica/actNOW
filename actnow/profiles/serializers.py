from rest_framework import serializers

from actnow.accounts.serializers import UserSerializer

from .models import OrganisationProfile, UserProfile


class OrganisationProfileSerializer(serializers.ModelSerializer):
    owners = UserSerializer(read_only=True, many=True)

    class Meta:
        model = OrganisationProfile
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not rep.get("name"):
            rep["name"] = str(instance)

        return rep

    class Meta:
        model = UserProfile
        fields = "__all__"
