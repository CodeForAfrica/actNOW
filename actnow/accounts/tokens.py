from django.conf import settings
from oauthlib.oauth2.rfc6749.tokens import (
    signed_token_generator as default_signed_token_generator,
)

signed_token_generator_handler = default_signed_token_generator(
    settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"]
)


def signed_token_generator(request, **kwargs):
    return signed_token_generator_handler(request, **kwargs)
