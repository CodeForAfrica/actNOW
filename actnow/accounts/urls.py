from django.urls import path

from .views import UserRegistrationView

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="accounts-user_registration"),
]
