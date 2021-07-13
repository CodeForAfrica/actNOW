from django.urls import path
from rest_framework import routers

from .views import PetitionView, SignatureView, follow_petition

router = routers.DefaultRouter()
router.register(r"petitions", PetitionView)
router.register(r"signatures", SignatureView)

urlpatterns = router.urls
urlpatterns += [path("<int:pk>/follow", follow_petition, name="follow_pettition")]
