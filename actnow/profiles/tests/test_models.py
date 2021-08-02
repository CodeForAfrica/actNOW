from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import models
from .model_factory import OrganisationProfileFactory, UserFactory

User = get_user_model()


class UserProfileTest(TestCase):
    def test_create_user_profile(self):
        # Creating a user account should automatically create a user profile
        User.objects.create_user(
            email="root@root.com", password="RandomPassword321", username="root"
        )
        self.assertEqual(1, models.UserProfile.objects.count())

    def test_validate_social_media_link(self):
        user = UserFactory()
        with self.assertRaises(ValidationError):
            user_profile = models.UserProfile(
                user=user,
                first_name="User1",
                social_media_link="https://invalidurl.com",
            )
            user_profile.full_clean()


class OrganisationProfileTestCase(TestCase):
    def test_create_organisation_profile(self):
        OrganisationProfileFactory()
        self.assertEqual(1, models.OrganisationProfile.objects.count())

    def test_organisation_can_not_have_more_than_2_owners(self):
        org = OrganisationProfileFactory()
        with self.assertRaises(ValidationError):
            for _ in range(3):
                org.owners.add(UserFactory())
