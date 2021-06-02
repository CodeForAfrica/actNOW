from django.contrib.auth import get_user_model

User = get_user_model()


def email_address_exists(email):
    return User.objects.filter(email=email).first()
