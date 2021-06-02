from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .utils import email_address_exists, username_exists

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        return email

    def validate_username(self, username):
        if username_exists(username):
            raise serializers.ValidationError(
                _("A user is already registered with this username"),
            )
        return username

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
