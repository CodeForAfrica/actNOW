from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class ActNowBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        """
        Use username to authenticate a user since we changed
        the default username to be email.
        """
        user = User.objects.filter(username=username).first()
        if not user:
            return None
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()
