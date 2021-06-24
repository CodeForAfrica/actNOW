from rest_framework import serializers

from actnow.accounts.serializers import UserSerializer

from .models import Petition, Signature


class SignatureSerializer(serializers.ModelSerializer):
    signatory = UserSerializer(read_only=True)

    class Meta:
        model = Signature
        fields = "__all__"


class PetitionSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
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
