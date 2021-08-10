from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from actnow.profiles.models import UserProfile

from .model_factory import UserFactory

User = get_user_model()


class TestUserProfileView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/v1/profiles/users/"
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.HTTP_AUTHORIZATION = f"Token {str(token)}"
        self.user_profile_data = {
            "first_name": "Test",
            "last_name": "Last",
            "location": "Kenya, Nairobi",
        }

    def test_edit_user_profile(self):
        self.assertEqual(1, UserProfile.objects.count())
        self.assertNotEqual("Test", self.user.userprofile.first_name)
        response = self.client.patch(
            f"{self.url}{self.user.userprofile.id}/",
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            data=self.user_profile_data,
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("Test", response.json().get("first_name"))


class TestOrganistionProfileView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/v1/profiles/organisations/"
        self.user = UserFactory()
        token = Token.objects.get(user=self.user)
        self.HTTP_AUTHORIZATION = f"Token {str(token)}"
        self.organisation_profile_data = {
            "name": "Code for Africa",
            "email": "test@codeforafrica.org",
            "website": "https://codeforafrica.org",
        }

    def test_create_organisation_profile(self):
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            data=self.organisation_profile_data,
        )
        self.assertEqual(201, response.status_code)
        organisation_profile = response.json()
        self.assertEqual("Code for Africa", organisation_profile.get("name"))
        # user making the request should be added as one of the owners
        self.assertEqual(1, len(organisation_profile["owners"]))
        self.assertEqual(self.user.email, organisation_profile["owners"][0]["email"])
