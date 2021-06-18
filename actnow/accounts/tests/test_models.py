from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class ActNowUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email="root@root.com", password="RandomPassword321"
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = self.User.objects.create_superuser(
            email="root@root.com", password="RandomPassword321"
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_is_required(self):
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                username="noemailuser", password="RandomPassword321"
            )

    def test_user_email_is_unique(self):
        self.User.objects.create_user(
            email="user@user.com", password="RandomPassword321"
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                email="user@user.com", password="RandomPassword321"
            )

    def test_username_is_unique(self):
        self.User.objects.create_user(
            username="butcher", email="butcher1@gmail.com", password="RandomPassword321"
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username="butcher",
                email="butcher2@gmail.com",
                password="RandomPassword321",
            )
