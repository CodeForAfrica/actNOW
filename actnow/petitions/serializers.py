from rest_framework import serializers

from actnow.accounts.serializers import UserRegistrationSerializer

from .models import Petition, Signature


class SignatureSerializer(serializers.ModelSerializer):
    signatory = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = Signature
        fields = "__all__"


class PetitionSerializer(serializers.ModelSerializer):
    owner = UserRegistrationSerializer(read_only=True)
    signatures = SignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Petition
        fields = [
            "created_at",
            "updated_at",
            "title",
            "description",
            "recipients",
            "problem_statement",
            "number_of_signatures_required",
            "image",
            "video",
            "owner",
            "signatures",
        ]
