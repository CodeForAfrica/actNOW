from rest_framework.routers import DefaultRouter

from .views import OrganisationProfileView

router = DefaultRouter()
router.register(
    r"organisations", OrganisationProfileView, basename="organisation_profile"
)

urlpatterns = router.urls
