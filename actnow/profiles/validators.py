from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_social_media_link(link):
    link = link.lower()
    if not any(["twitter" in link, "facebook" in link, "whatsapp" in link]):
        raise ValidationError(
            _("%(link)s is not a valid social media link."),
            params={"link": link},
        )
