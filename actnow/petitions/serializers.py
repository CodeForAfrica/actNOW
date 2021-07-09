from rest_framework import serializers

from actnow.accounts.serializers import UserSerializer

from .models import Issue, Petition, Signature


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class SignatureSerializer(serializers.ModelSerializer):
    signatory = UserSerializer(read_only=True)

    class Meta:
        model = Signature
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.anonymous:
            rep.pop("signatory")
        return rep


class PetitionSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    signatures = SignatureSerializer(many=True, read_only=True)
    issue = IssueSerializer()

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
            "issue",
        ]
