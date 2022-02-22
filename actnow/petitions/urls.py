from django.urls import path
from rest_framework import routers

from .views import follow_petition
from .viewsets import PetitionViewSet, SignatureViewSet

router = routers.DefaultRouter()
router.register(r"signatures", SignatureViewSet)
router.register(r"", PetitionViewSet, basename="petitions")

urlpatterns = router.urls
urlpatterns += [path("<int:pk>/followers", follow_petition, name="petition_followers")]
