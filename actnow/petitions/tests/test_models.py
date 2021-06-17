from ..models import Petition
from django.db.utils import IntegrityError
 
from django.test import TestCase

class PetitionTest(TestCase):
    def test_create_petition(self):
        Petition.objects.create(
            title="Petition A",
            problem_statement="Problem Statement",
            description="Details of Petition",
            recipients="City Council",
        )
        self.assertEqual(1, Petition.objects.count())

    def test_petition_is_unique(self):
        Petition.objects.create(
            title="Petition B",
            problem_statement="Petitioning Issue",
            description="Description",
            recipients="Member of Parliament",
        )

        with self.assertRaises(IntegrityError):
            Petition.objects.create(
                title="Petition B",
                problem_statement="Problem Statement",
                description="Details of Petition",
                recipients="City Council",
            )

