import random
import string

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from oauth2_provider.models import get_application_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from actnow.petitions.models import Petition

User = get_user_model()


class TestPetitionView(TestCase):
    def setUp(self):
        user_data = {
            "email": "test_user@email.com",
            "password": "".join(
                random.choices(string.ascii_uppercase + string.digits, k=12)
            ),
        }
        user = User.objects.create_user(**user_data)
        self.application = get_application_model()(user=user)
        self.application.save()
        self.token = Token.objects.get(user=user.id)
        self.HTTP_AUTHORIZATION = f"Token {self.token}"
        self.url = reverse("petitions-list")
        self.client = APIClient()
        self.data = {
            "title": "title",
            "description": "description",
            "recipients": "recipients",
            "problem_statement": "problem statement",
            "number_of_signatures_required": 0,
            "source": {
                "link": "https://codeforafrica.org",
            },
        }

    def test_create_fails_for_unauthenticated_users(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_passes_for_authenticated_users(self):
        response = self.client.post(
            self.url,
            self.data,
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, Petition.objects.count())

    def test_list(self):
        unauthenticated_response = self.client.get(self.url)
        self.assertEqual(unauthenticated_response.status_code, 200)
        authenticated_response = self.client.get(
            self.url,
            self.data,
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            format="json",
        )
        self.assertEqual(authenticated_response.status_code, 200)
        self.assertEqual(
            len(unauthenticated_response.data), len(authenticated_response.data)
        )
        self.assertEqual(len(authenticated_response.data), Petition.objects.count())
