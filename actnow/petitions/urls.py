from django.urls import include, path
from rest_framework import routers

from .views import PetitionSignatureView, PetitionView

router = routers.DefaultRouter()
router.register(r"", PetitionView)
router.register(r"signatures", PetitionSignatureView)

urlpatterns = [
    path("", include(router.urls)),
]
