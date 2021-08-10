import factory
from django.contrib.auth import get_user_model

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = (
            "email",
            "username",
        )

    email = factory.Sequence(lambda n: "user{}@example.com".format(n))
    username = factory.Faker("name")


class OrganisationProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrganisationProfile

    name = factory.Faker("name")
    bio = factory.Faker("text")
    email = factory.Faker("email")
    photo = factory.django.ImageField(width=1024, height=768)
    website = factory.Faker("url")
    social_media_link = factory.Faker("url")
