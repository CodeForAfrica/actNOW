from django.contrib.auth import get_user_model
from django.test import TestCase

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

        self.signatory = ActNowUser.objects.create_user(
            email="test@gmail.com", username="test", password="test2021?"
        )

    def test_str_petition(self):
        p = Petition.objects.create(
            title="Petition A",
            problem_statement="Problem Statement",
            description="Details of Petition",
            recipients="City Council",
        )
        self.assertEqual(str(p), "Petition A")

    def test_create_signature(self):
        Signature.objects.create(
            petition=self.petition,
            signatory=self.signatory,
            comment="I signed because..",
        )
        self.assertEqual(1, Signature.objects.count())
