from django.contrib import admin

from .models import Location, Socials, UserProfile

admin.site.register([UserProfile, Location, Socials])
