from django_filters import rest_framework as filters

from .models import Petition


class PetitionFilter(filters.FilterSet):
    individual_signatories = filters.NumberFilter(
        field_name="signatures__signatory__user_profile"
    )
    organisation_signatories = filters.NumberFilter(
        field_name="signatures__signatory__organisation_profile"
    )

    class Meta:
        model = Petition
        fields = [
            "owner",
            "followers",
            "individual_signatories",
            "organisation_signatories",
        ]
