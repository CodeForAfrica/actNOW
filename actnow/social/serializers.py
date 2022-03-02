from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from rest_framework import serializers


class UserDetailsSerializer(BaseUserDetailsSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return {
            "id": obj.userprofile.id,
        }

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = BaseUserDetailsSerializer.Meta.fields + ("profile",)
