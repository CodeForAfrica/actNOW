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
    photo = models.ImageField(max_length=30)
    location = models.TextField()
    phone_number = PhoneNumberField(blank=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Organisation(models.Model):
    name = models.CharField(max_length=20)
    website_link = models.URLField(blank=True, null=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True, null=True
    )
    person_1 = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, related_name="person_1", null=True
    )
    person_2 = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, related_name="person_2", null=True
    )

    def __str__(self):
        return self.name
