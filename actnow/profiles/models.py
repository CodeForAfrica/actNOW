from django.db import models

from .validators import phone_regex


class UserProfile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(
        verbose_name="About me", max_length=255, blank=True, null=True
    )
    location = models.TextField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    socials = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
