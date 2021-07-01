from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from actnow.db.models import TimestampedModelMixin

from .validators import validate_social_media_link


class UserProfile(TimestampedModelMixin):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, null=True, blank=True)
    bio = models.TextField(_("about me"), max_length=255, blank=True, null=True)
    photo = models.ImageField(_("photo"), blank=True, null=True)
    location = models.TextField(_("location"), max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True, null=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrganisationProfile(TimestampedModelMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    photo = models.ImageField(_("photo"), blank=True)
    website = models.URLField(_("website"), unique=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True
    )
    persons = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.name
