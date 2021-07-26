import uuid

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class ActNowUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email="user@email.com",
            username="user",
            password="RandomPassword321",
            # is_superuser must always be set to False in create_user
            # regardless of what value was passed in.
            is_superuser=True,
        )

        # If username is provided, it must be preserved
        self.assertEqual(user.username, "user")
        self.assertEqual(user.email, "user@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_username(self):
        user = self.User.objects.create_user(
            email="user@email.com", password="RandomPassword321"
        )

        # If no username was provided, uuid4 must be used to generate a random
        # username.
        self.assertIsNotNone(user.username)
        self.assertEqual(uuid.UUID(user.username).version, 4)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = self.User.objects.create_superuser(
            email="root@email.com", username="root", password="RandomPassword321"
        )

        # If username is provided, it must be preserved
        self.assertEqual(user.username, "root")
        self.assertEqual(user.email, "root@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_username(self):
        user = self.User.objects.create_superuser(
            email="root@email.com", password="RandomPassword321"
        )

        # If no username was provided, uuid4 must be used to generate a random
        # username.
        self.assertIsNotNone(user.username)
        self.assertEqual(uuid.UUID(user.username).version, 4)
        self.assertTrue(user.is_superuser)

    def test_email_is_required(self):
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                username="noemailuser", password="RandomPassword321"
            )

    def test_email_is_unique(self):
        self.User.objects.create_user(
            email="user@email.com", username="user1", password="RandomPassword1"
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                email="user@email.com", username="user2", password="RandomPassword2"
            )

    def test_username_is_unique(self):
        self.User.objects.create_user(
            email="user1@email.com", username="user", password="RandomPassword1"
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                email="user2@email.com",
                username="user",
                password="RandomPassword2",
            )
