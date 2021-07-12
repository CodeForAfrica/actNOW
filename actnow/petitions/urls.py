from rest_framework import routers

from .views import PetitionView, SignatureView

router = routers.DefaultRouter()
router.register(r"petitions", PetitionView)
router.register(r"signatures", SignatureView)

urlpatterns = router.urls
