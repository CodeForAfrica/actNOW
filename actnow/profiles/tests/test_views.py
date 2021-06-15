from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse
from django.utils import timezone
from oauth2_provider.models import get_application_model, get_id_token_model
from rest_framework.test import force_authenticate

from ..views import UserProfileView
from .model_factory import UserFactory


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
        application = get_application_model()()
        application.save()
        expires = timezone.now() + timezone.timedelta(seconds=10)
        id_token = get_id_token_model()(application=application, expires=expires)
        id_token.save()
        assert id_token.is_valid()
        request = self.factory.post(
            self.url,
            {**self.user_profile, **{"user": user.id, "id_token": str(id_token.jti)}},
            format="multipart/form-data",
        )
        force_authenticate(request, user=user)
        response = self.user_profile_view(request)
        self.assertEqual(201, response.status_code)
