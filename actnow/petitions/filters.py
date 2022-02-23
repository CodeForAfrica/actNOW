from django_filters import rest_framework as filters

from .models import Petition


class PetitionFilter(filters.FilterSet):
    user_profile = filters.CharFilter(field_name="signatures__signatory__user_profile")
    organisation_profile = filters.CharFilter(
        field_name="signatures__signatory__organisation_profile"
    )

    class Meta:
        model = Petition
        fields = ["owner", "followers", "user_profile", "organisation_profile"]
