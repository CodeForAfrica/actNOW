from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .validators import validate_social_media_link


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(
        verbose_name="About me", max_length=255, blank=True, null=True
    )
    photo = models.ImageField(max_length=30, null=True, blank=True)
    location = models.TextField()
    phone_number = PhoneNumberField(blank=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrganisationProfile(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    photo = models.ImageField(max_length=50)
    website = models.URLField(blank=True, null=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True, null=True
    )
    persons = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name
