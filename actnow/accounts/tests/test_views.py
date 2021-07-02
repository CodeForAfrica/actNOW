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
        user = User.objects.create_superuser(
            email="test_user@test.org", username="test_user"
        )
        self.application = get_application_model()(user=user)
        self.application.save()
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
        user = User.objects.create_superuser(
            email="superuser@test.org", username="superuser"
        )
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
        update_data = {
            "username": "new_user_name",
        }

        user = User.objects.get(email="testuser@mail.com")

        response = self.client.patch(f"{self.url}{user.id}/", data=update_data)
        self.assertEqual(401, response.status_code)
        # Create an AccessToken.
        # In real world,
        # this will be generated after the user manually accepts the OAuth prompt.
        expires = timezone.now() + timezone.timedelta(seconds=100)
        oauth_access_token = AccessToken(token=self.token, expires=expires, user=user)
        oauth_access_token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(oauth_access_token.token)
        )
        response = self.client.patch(f"{self.url}{user.id}/", data=update_data)
        self.assertEqual(200, response.status_code)
        # check username has been updated
        response = self.client.get(f"{self.url}{user.id}/")
        self.assertEqual(update_data["username"], response.json()["username"])

    def test_only_account_owners_can_delete_their_accounts(self):
        # Register user
        self.client.post(
            self.url, self.user_data, HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        user = User.objects.get(email="testuser@mail.com")
        # Try deleting account using an admin token
        response = self.client.delete(
            f"{self.url}{user.id}/", HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(403, response.status_code)
        # Create an AccessToken.
        # In real world,
        # this will be generated after the user manually accepts the OAuth prompt.
        expires = timezone.now() + timezone.timedelta(seconds=100)
        oauth_access_token = AccessToken(token=self.token, expires=expires, user=user)
        oauth_access_token.save()
        # delete account using OAuth token
        response = self.client.delete(
            f"{self.url}{user.id}/",
            HTTP_AUTHORIZATION="Bearer " + str(oauth_access_token.token),
        )
        self.assertEqual(204, response.status_code)
        # Ensure account has been deleted
        response = self.client.get(
            f"{self.url}{user.id}/", HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION
        )
        self.assertEqual(404, response.status_code)

        # ensure once an account is deleted, all tokens are revoked.
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer " + str(oauth_access_token.token),
        )
        self.assertEqual(401, response.status_code)
        with self.assertRaises(AccessToken.DoesNotExist):
            oauth_access_token.refresh_from_db()
