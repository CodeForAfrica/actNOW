from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import get_id_token_model
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class CustomApplicationAuthentication(TokenAuthentication):
    """
    Authenticates using JWT ID since we don't have a user associated
    with an application that we can use to generate DRF Token.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

    """

    def authenticate_credentials(self, key):
        model = get_id_token_model()
        try:
            token = model.objects.select_related("application").get(jti=key)
        except Exception:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.is_valid:
            raise exceptions.AuthenticationFailed(_("Application inactive or deleted."))

        return (token.application, token)
