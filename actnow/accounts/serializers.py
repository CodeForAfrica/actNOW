from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        request_data = self.context["request"].data.copy()
        # Remove user account data
        [request_data.pop(f, None) for f in self.fields]

        user = User.objects.create_user(**validated_data, request_data=request_data)

        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            del validated_data["password"]
        return super().update(instance, validated_data)
