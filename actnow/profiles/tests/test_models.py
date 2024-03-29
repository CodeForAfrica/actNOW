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
        user_profiles = models.UserProfile.objects.all()
        profiles = models.Profile.objects.all()
        self.assertEqual(1, len(user_profiles))
        self.assertEqual(1, len(profiles))
        self.assertEqual(user_profiles[0], profiles[0].user_profile)
        self.assertIsNone(profiles[0].organisation_profile)

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
        org_profiles = models.OrganisationProfile.objects.all()
        profiles = models.Profile.objects.all()
        self.assertEqual(1, len(org_profiles))
        self.assertEqual(1, len(profiles))
        self.assertEqual(org_profiles[0], profiles[0].organisation_profile)
        self.assertIsNone(profiles[0].user_profile)

    def test_organisation_can_not_have_more_than_2_owners(self):
        org = OrganisationProfileFactory()
        with self.assertRaises(ValidationError):
            for _ in range(3):
                org.owners.add(UserFactory())
