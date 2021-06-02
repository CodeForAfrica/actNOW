from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

User = get_user_model()


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "TestUser",
            "email": "testuser@mail.com",
            "password": "RandomPassword#2323#",
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
