from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from actnow.db.models import TimestampedModelMixin

from .validators import validate_social_media_link

User = get_user_model()


class Profile(TimestampedModelMixin):
    bio = models.TextField(_("bio"), max_length=255, blank=True)
    photo = models.ImageField(_("photo"), blank=True)
    location = models.TextField(_("location"), max_length=255, blank=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True
    )

    class Meta:
        abstract = True


class OrganisationProfile(Profile):
    owners = models.ManyToManyField(User)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    # For organisation profile, we do need a unique website/domain
    website = models.URLField(_("website"), unique=True)

    def __str__(self):
        return self.name


class UserProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    # This is the prefered name. If left blank, first_name + last_name will be used.
    name = models.CharField(_("name"), max_length=255, blank=True)
    # For normal user profile, lets relax the unique requirement for websites
    website = models.URLField(_("website"), blank=True)

    def __str__(self):
        return self.name or " ".join(filter(None, (self.first_name, self.last_name)))
