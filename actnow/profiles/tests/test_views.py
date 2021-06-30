from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from actnow.profiles.models import UserProfile

from .model_factory import UserFactory

User = get_user_model()


class TestUserProfileView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user_profile-list")
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.HTTP_AUTHORIZATION = f"Token {str(token)}"
        self.user_profile_data = {
            "first_name": "Test",
            "last_name": "Last",
            "location": "Kenya, Nairobi",
        }

    def test_create_user_profile(self):
        self.assertEqual(0, UserProfile.objects.count())
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            data=self.user_profile_data,
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, UserProfile.objects.count())