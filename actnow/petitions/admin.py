from django.contrib import admin

from .models import Petition, PetitionSignature

admin.site.register(Petition)
admin.site.register(PetitionSignature)
