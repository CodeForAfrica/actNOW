from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if not validated_data["username"]:
            del validated_data["username"]

        request_data = self.context["request"].data.copy()
        # Remove user account data
        request_data.pop("username")
        request_data.pop("email")
        request_data.pop("password")
        user = User.objects.create_user(**validated_data, request_data=request_data)

        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            del validated_data["password"]
        return super().update(instance, validated_data)
