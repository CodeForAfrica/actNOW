from django.urls import include, path

from .views import GoogleLogin

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
