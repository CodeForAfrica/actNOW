from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username"),
            "password": self.validated_data.get("password"),
            "email": self.validated_data.get("email"),
        }

    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        if not cleaned_data["username"]:
            del cleaned_data["username"]

        user = User.objects.create_user(**cleaned_data)
        return user
