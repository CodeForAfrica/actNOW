from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from actnow.db.models import TimestampedModelMixin

from .validators import validate_social_media_link

User = get_user_model()


class ProfileMixin(TimestampedModelMixin):
    bio = models.TextField(_("bio"), max_length=255, blank=True)
    photo = models.ImageField(_("photo"), blank=True)
    location = models.TextField(_("location"), max_length=255, blank=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True)
    social_media_link = models.URLField(
        validators=[validate_social_media_link], blank=True
    )

    class Meta:
        abstract = True


class OrganisationProfile(ProfileMixin):
    owners = models.ManyToManyField(User)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    # For organisation profile, we do need a unique website/domain
    website = models.URLField(_("website"), unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self._state.adding
        super().save(*args, **kwargs)
        if created:
            profile = Profile(organisation_profile=self)
            profile.save()


class UserProfile(ProfileMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    # This is the prefered name. If left blank, first_name + last_name will be used.
    name = models.CharField(_("name"), max_length=255, blank=True)
    # For normal user profile, lets relax the unique requirement for websites
    website = models.URLField(_("website"), blank=True)

    def __str__(self):
        return self.name or " ".join(filter(None, (self.first_name, self.last_name)))

    def save(self, *args, **kwargs):
        created = self._state.adding
        super().save(*args, **kwargs)
        if created:
            profile = Profile(user_profile=self)
            profile.save()


NUM_NONNULLS_SQL = (
    "num_nonnulls(organisation_profile_id::bigint , user_profile_id::bigint) = 1"
)


class Profile(TimestampedModelMixin):
    organisation_profile = models.OneToOneField(
        OrganisationProfile,
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )

    def __str__(self):
        if self.organisation_profile:
            return str(self.organisation_profile)

        return str(self.user_profile)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=RawSQL(
                    NUM_NONNULLS_SQL,
                    params=(),
                    output_field=models.BooleanField(),
                ),
                name="single_unique_profile",
            ),
        ]
