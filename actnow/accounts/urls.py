from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UsersView

router = DefaultRouter()
router.register(r"", UsersView, basename="accounts")

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
]

urlpatterns += router.urls
