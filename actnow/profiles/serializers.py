from rest_framework import serializers

from actnow.accounts.serializers import UserSerializer

from .models import OrganisationProfile, Profile, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        if instance.organisation_profile:
            return OrganisationProfileSerializer(
                instance=instance.organisation_profile
            ).data

        if instance.user_profile:
            return UserProfileSerializer(instance=instance.user_profile).data

        return super().to_representation(instance)


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
