from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def generate_user_token(sender, **kwargs):
    user = kwargs["instance"]
    Token.objects.create(user=user)
