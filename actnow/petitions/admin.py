from django.contrib import admin

from .models import Petition, Signature

admin.site.register([Petition, Signature])
