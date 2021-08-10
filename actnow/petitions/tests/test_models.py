from django.contrib.auth import get_user_model
from django.test import TestCase

from actnow.profiles.models import Profile, UserProfile

from ..models import Petition, Signature

ActNowUser = get_user_model()


class PetitionTest(TestCase):
    def setUp(self):
        self.petition = Petition.objects.create(
            title="Petition A",
            problem_statement="Problem Statement",
            description="Details of Petition",
            recipients="City Council",
        )

        user = ActNowUser.objects.create_user(
            email="test@gmail.com", username="test", password="test2021?"
        )
        user_profile = UserProfile.objects.get(user=user)
        self.profile = Profile.objects.get(user_profile=user_profile)

    def test_str_petition(self):
        p = Petition.objects.create(
            title="Petition A",
            problem_statement="Problem Statement",
            description="Details of Petition",
            recipients="City Council",
            owner=self.profile,
        )
        self.assertEqual(str(p), "Petition A by test")

    def test_create_signature(self):
        Signature.objects.create(
            petition=self.petition,
            signatory=self.profile,
            comment="I signed because..",
        )
        self.assertEqual(1, Signature.objects.count())
