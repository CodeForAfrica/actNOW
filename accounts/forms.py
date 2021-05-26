from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ActNowUser


class ActNowUserCreationForm(UserCreationForm):
    class Meta:
        model = ActNowUser
        fields = ("email",)


class ActNowUserChangeForm(UserChangeForm):
    class Meta:
        model = ActNowUser
        fields = ("email",)
