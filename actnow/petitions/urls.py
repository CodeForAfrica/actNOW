from django.urls import include, path
from rest_framework import routers

from .views import PetitionView, PetitionSignatureView

router = routers.DefaultRouter()
router.register(r'petitions', PetitionView)

urlpatterns = [
    path("", include(router.urls)),
    path("signatures/", PetitionSignatureView.as_view(), name="petition-signatures")
]
