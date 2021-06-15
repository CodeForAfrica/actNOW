from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone
from oauth2_provider.models import get_application_model, get_id_token_model

User = get_user_model()


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.application = get_application_model()()
        self.application.save()
        expires = timezone.now() + timezone.timedelta(seconds=10)
        self.id_token = get_id_token_model()(
            application=self.application, expires=expires
        )
        self.id_token.save()
        self.user_data = {
            "username": "TestUser",
            "email": "testuser@mail.com",
            "password": "RandomPassword#2323#",
            "application_token": str(self.id_token.jti),
        }
        self.url = reverse("accounts-user_registration")

    def test_user_registration(self):
        self.assertEqual(0, User.objects.count())
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_existing_email_returns_error(self):
        self.client.post(self.url, self.user_data)
        self.assertEqual(1, User.objects.count())
        self.user_data["username"] = "tester2"
        response = self.client.post(self.url, self.user_data)
        self.assertIn(
            b"A user is already registered with this e-mail address.", response.content
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_existing_username_returns_error(self):
        self.client.post(self.url, self.user_data)
        self.assertEqual(1, User.objects.count())
        self.user_data["email"] = "tester2@mail.com"
        response = self.client.post(self.url, self.user_data)
        self.assertIn(
            b"A user is already registered with this username", response.content
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_only_apps_can_register_a_user(self):
        user_data = {**self.user_data}
        del user_data["application_token"]
        response = self.client.post(self.url, user_data)
        self.assertEqual(401, response.status_code)
