from rest_framework.routers import DefaultRouter

from .views import OrganisationProfileView, ProfileView, UserProfileView

router = DefaultRouter()
router.register(
    r"organisations", OrganisationProfileView, basename="organisation_profile"
)
router.register(r"users", UserProfileView, basename="user_profile")
router.register(r"", ProfileView)

urlpatterns = router.urls
