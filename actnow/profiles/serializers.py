from rest_framework import serializers

from .models import OrganisationProfile


class OrganisationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationProfile
        fields = "__all__"
