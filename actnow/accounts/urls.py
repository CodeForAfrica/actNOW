from rest_framework.routers import DefaultRouter

from .views import UsersView

router = DefaultRouter()
router.register(r"", UsersView, basename="accounts")

urlpatterns = router.urls
