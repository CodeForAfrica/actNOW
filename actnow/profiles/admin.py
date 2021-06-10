from django.contrib import admin

from .models import Organisation, UserProfile

admin.site.register(
    [
        UserProfile,
        Organisation,
    ]
)
