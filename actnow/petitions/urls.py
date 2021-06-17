from django.urls import include, path
from rest_framework import routers

from .views import PetitionView, SignatureView

router = routers.DefaultRouter()
router.register(r"", PetitionView)
router.register(r"signatures", SignatureView)

urlpatterns = [
    path("", include(router.urls)),
]
