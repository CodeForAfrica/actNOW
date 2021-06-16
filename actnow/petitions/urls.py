from django.urls import path

from .views import PetitionView, PetitionSignatorView

urlpatterns = [
    path("", PetitionView.as_view(), name="petition"),
    path("/sign", PetitionSignatorView.as_view(), name="petition")
]
