from django.contrib import admin

from .models import Issue, Petition, Signature

admin.site.register([Petition, Signature, Issue])
