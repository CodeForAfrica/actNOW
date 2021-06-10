from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import models
from .model_factory import UserProfileFactory


class UserProfileTest(TestCase):
    def test_create_user_profile(self):
        UserProfileFactory()
        self.assertEqual(1, models.UserProfile.objects.count())

    def test_validate_social_media_link(self):
        with self.assertRaises(ValidationError):
            user_profile = UserProfileFactory(
                social_media_link="https://invalidurl.com/userp"
            )
            user_profile.full_clean()

        valid_user_profile = UserProfileFactory(
            social_media_link="https://twitter.com/userprofile"
        )
        self.assertIsNone(valid_user_profile.full_clean())
