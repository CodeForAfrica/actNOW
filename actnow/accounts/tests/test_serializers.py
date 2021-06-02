from django.contrib.auth import get_user_model
from django.test import TestCase

from actnow.accounts.serializers import UserRegistrationSerializer

User = get_user_model()


class TestUserRegistrationSerializer(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "TestUser",
            "email": "testuser@mail.com",
            "password": "RandomPassword#2323#",
        }

    def test_email_is_required(self):
        del self.user_data["email"]
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_registration_serializer_save(self):
        self.assertEqual(0, User.objects.count())
        serializer = UserRegistrationSerializer(data=self.user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save({})
        self.assertEqual(1, User.objects.count())
