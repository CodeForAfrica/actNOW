from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import models
from .model_factory import OrganisationProfileFactory, UserFactory, UserProfileFactory


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


class OrganisationProfileTest(TestCase):
    def test_create_organisation_profile(self):
        OrganisationProfileFactory()
        self.assertEqual(1, models.OrganisationProfile.objects.count())

    def test_organisation_can_not_have_more_than_2_people(self):
        org = OrganisationProfileFactory()
        with self.assertRaises(ValidationError):
            for _ in range(3):
                org.persons.add(UserFactory())
