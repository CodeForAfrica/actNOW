from rest_framework import serializers
from .models import Petition, PetitionSignature


class PetitionSerializer(serializers.Serializer):
    class Meta:
        model = Petition
        fields = [
            "title",
            "description",
            "owner",
            "recipients",
            "problem_to_address",
            "number_of_signature_required",
            "image",
            "video",
        ]


class PetitionSignatureSerializer(serializers.Serializer):
    class Meta:
        model = PetitionSignature
        fields = ['petition', 'signator', 'comment']

