from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import OrganisationProfile


@receiver(m2m_changed, sender=OrganisationProfile.persons.through)
def number_of_organisations_changed(sender, **kwargs):
    if kwargs["action"] == "post_add":
        if sender.objects.count() > 2:
            raise ValidationError("Can only have two people in an organisation.")

    if kwargs["action"] == "post_remove":
        if sender.objects.count() < 1:
            raise ValidationError("An Organisation must have at least one person.")
