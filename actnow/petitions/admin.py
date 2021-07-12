from django.contrib import admin

from .models import Petition, Signature, Source

admin.site.register([Petition, Signature, Source])
