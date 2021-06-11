import factory
from django.contrib.auth import get_user_model

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: "user{}@example.com".format(n))


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserProfile

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    location = "Kenya, Nairobi"
    social_media_link = factory.Faker("url")
    photo = factory.django.ImageField(width=1024, height=768)
    user = factory.SubFactory(UserFactory)


class OrganisationProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrganisationProfile

    name = factory.Faker("name")
    description = factory.Faker("text")
    email = factory.Faker("email")
    photo = factory.django.ImageField(width=1024, height=768)
    website = factory.Faker("url")
    social_media_link = factory.Faker("url")
class AdminUserFactory(UserFactory):
    is_staff = True
