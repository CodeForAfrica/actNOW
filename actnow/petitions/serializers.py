from rest_framework import serializers
from .model import Petition, PetitionSignator


class PetitionSerializer(serializers.Serializer):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'owner', 'recipients', 'problem_to_address', 'number_of_signature_required', 'image', 'video']


class PetitionSignatorSerializer(serializers.Serializer):
    class Meta:
        model = PetitionSignator
        fields = ['petition', 'signator', 'comment']

