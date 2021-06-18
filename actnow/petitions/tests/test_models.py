from django.test import TestCase

from ..models import Petition


class PetitionTest(TestCase):
    def test_create_petition(self):
        Petition.objects.create(
            title="Petition A",
            problem_statement="Problem Statement",
            description="Details of Petition",
            recipients="City Council",
        )
        self.assertEqual(1, Petition.objects.count())
