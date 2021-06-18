import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, get_application_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "TestUser",
            "email": "testuser@mail.com",
            "password": "RandomPassword#2323#",
        }
        self.url = reverse("accounts-list")
        user = User.objects.create_superuser(email="test_user@test.org")
        application = get_application_model()(user=user)
        application.save()
        self.token = Token.objects.get(user=user.id)
        self.HTTP_AUTHORIZATION = f"Token {self.token}"

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
        self.assertIn(b"user with this email address already exists.", response.content)
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
        self.assertIn(b"A user with that username already exists.", response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())

    def test_only_an_application_can_register_a_new_user(self):
        # A super user with no application
        user = User.objects.create_superuser(email="superuser@test.org")
        super_user_token = Token.objects.get(user=user.id)
        HTTP_AUTHORIZATION = f"Token {super_user_token}"
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=HTTP_AUTHORIZATION
        )
        self.assertEqual(403, response.status_code)

        # User with an associated application
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(201, response.status_code)

    def test_any_logged_in_user_can_view_other_users(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(401, response.status_code)
        response = self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(201, response.status_code)

    def test_only_an_account_owner_can_update_their_accounts_using_oauth_token(self):
        # Register user
        self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        update_data = json.dumps(
            {
                "username": "new_user_name",
            }
        )
        response = self.client.patch(self.url, update_data, format="json")
        self.assertEqual(401, response.status_code)
        expires = timezone.now() + timezone.timedelta(seconds=100)
        user = User.objects.get(email="testuser@mail.com")
        # Create an AccessToken.
        # In real world,
        # this will be generated after the user manually accepts the OAuth prompt.
        oauth_access_token = AccessToken(token=self.token, expires=expires, user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(oauth_access_token.token)}"
        )
        response = self.client.patch(
            self.url,
            update_data,
            format="json",
        )
