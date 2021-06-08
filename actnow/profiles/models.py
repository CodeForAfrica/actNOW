from django.db import models
from django_countries.fields import CountryField

from .validators import phone_regex


class UserProfile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(
        verbose_name="About me", max_length=255, blank=True, null=True
    )
    location = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    socials = models.OneToOneField("Socials", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    country = CountryField()
    county = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.country.name


class Socials(models.Model):
    class Meta:
        verbose_name_plural = "Socials"

    facebook = models.CharField(max_length=20, unique=True, blank=True, null=True)
    instagram = models.CharField(max_length=20, unique=True, blank=True, null=True)
    twitter = models.CharField(max_length=20, unique=True, blank=True, null=True)
    linkedin = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.facebook or self.instagram or self.twitter or self.facebook
