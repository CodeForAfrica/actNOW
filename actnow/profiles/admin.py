from django.contrib import admin

from .models import OrganisationProfile, UserProfile

admin.site.register(
    [
        UserProfile,
        OrganisationProfile,
    ]
)
