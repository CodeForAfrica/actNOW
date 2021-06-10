from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_social_media_link(link):
    link = link.lower()
    is_twitter = (
        link.startswith("https://twitter.com")
        or link.startswith("http://twitter.com")
        or link.startswith("https://mobile.twitter.com")
        or link.startswith("http://mobile.twitter.com")
    )
    is_facebook = (
        link.startswith("https://facebook.com")
        or link.startswith("http://facebook.com")
        or link.startswith("https://mobile.facebook.com")
        or link.startswith("http://mobile.facebook.com")
    )
    is_whatsapp = (
        link.startswith("https://wa.me")
        or link.startswith("http://wa.me")
        or link.startswith("https://api.whatsapp.com")
        or link.startswith("http://api.whatsapp.com")
    )

    if not any([is_twitter, is_facebook, is_whatsapp]):
        raise ValidationError(
            _("%(link)s is not a valid social media link."),
            params={"link": link},
        )
