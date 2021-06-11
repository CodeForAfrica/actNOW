from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse
from rest_framework.test import force_authenticate

from ..views import UserProfileView
from .model_factory import AdminUserFactory, UserFactory


class TestUserProfile(TestCase):
    def setUp(self):
        self.url = reverse("users_profiles")

        self.user_profile = {
            "first_name": "TestUser",
            "last_name": "TestUserLastName",
            "location": "Kenya, Nairobi",
        }
        self.factory = RequestFactory()
        self.user_profile_view = UserProfileView.as_view()

    def test_authetication_is_required_to_create_user_profile(self):
        response = self.client.post(self.url, self.user_profile)
        self.assertEqual(401, response.status_code)

    def test_user_profile_creation(self):
        user = UserFactory()
        request = self.factory.post(
            self.url, {**self.user_profile, **{"user": user.id}}, format="multipart"
        )
        force_authenticate(request, user=user)
        response = self.user_profile_view(request)
        self.assertEqual(201, response.status_code)

    def test_only_admins_can_query_all_user_profiles(self):
        user = UserFactory()
        request = self.factory.get(self.url)
        force_authenticate(request, user=user)
        response = self.user_profile_view(request)
        self.assertEqual(403, response.status_code)
        admin_user = AdminUserFactory()
        force_authenticate(request, user=admin_user)
        response = self.user_profile_view(request)
        self.assertEqual(200, response.status_code)
