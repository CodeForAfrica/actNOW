from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import OrganisationProfile
from .serializers import UserProfileSerializer

User = get_user_model()


@receiver(m2m_changed, sender=OrganisationProfile.persons.through)
def number_of_organisations_changed(sender, **kwargs):
    if kwargs["action"] == "post_add":
        if sender.objects.count() > 2:
            raise ValidationError("Can only have two people in an organisation.")

    if kwargs["action"] == "post_remove":
        if sender.objects.count() < 1:
            raise ValidationError("An Organisation must have at least one person.")


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        if hasattr(instance, "extra_fields"):
            data = instance.extra_fields.get("request_data", {})
            data["user"] = instance.id
            if not data.get("first_name"):
                data["first_name"] = instance.username
        else:
            data = {"user": instance.id, "first_name": instance.username}
        user_profile_serializer = UserProfileSerializer(data=data)

        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()
