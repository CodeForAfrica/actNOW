from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from oauth2_provider.models import get_application_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "TestUser",
            "email": "testuser@mail.com",
            "password": "RandomPassword#2323#",
        }
        self.url = reverse("accounts-user_registration")
        user = User.objects.create_superuser(email="test_user@test.org")
        application = get_application_model()(user=user)
        application.save()
        token = Token.objects.get(user=user.id)
        self.HTTP_AUTHORIZATION = f"Token {token}"

    def test_user_registration(self):
        self.assertEqual(1, User.objects.count())
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, User.objects.count())

    def test_existing_email_returns_error(self):
        self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(2, User.objects.count())
        self.user_data["username"] = "tester2"
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertIn(
            b"A user is already registered with this e-mail address.", response.content
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())

    def test_existing_username_returns_error(self):
        self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(2, User.objects.count())
        self.user_data["email"] = "tester2@mail.com"
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertIn(
            b"A user is already registered with this username", response.content
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())
