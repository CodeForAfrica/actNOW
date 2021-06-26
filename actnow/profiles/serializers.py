from rest_framework import serializers

from .models import OrganisationProfile, UserProfile


class OrganisationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationProfile
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = "__all__"
