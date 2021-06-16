from django.urls import path
from rest_framework.authtoken import views

from .views import UserRegistrationView

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="accounts-user_registration"),
    path("api-token-auth/", views.obtain_auth_token),
]
