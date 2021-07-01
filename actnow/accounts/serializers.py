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

        request_data = self.context["request"].data

        first_name = request_data.get("first_name", validated_data["username"])
        last_name = request_data.get("last_name", "")
        bio = request_data.get("bio", "")
        photo = request_data.get("photo", "")
        location = request_data.get("location", "")
        phone_number = request_data.get("phone_number", "")
        social_media_link = request_data.get("social_media_link", "")

        user = User.objects.create_user(
            **{
                **validated_data,
                **{
                    "first_name": first_name,
                    "last_name": last_name,
                    "bio": bio,
                    "photo": photo,
                    "location": location,
                    "phone_number": phone_number,
                    "social_media_link": social_media_link,
                },
            }
        )

        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            del validated_data["password"]
        return super().update(instance, validated_data)
