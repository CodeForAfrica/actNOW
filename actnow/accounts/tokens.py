from django.conf import settings
from oauthlib import common


def signed_token_generator(request, **kwargs):
    request.claims = {
        "aud": request.client.client_id,
        "iss": "actNOW",
        "sub": request.user.id,
        "scope": " ".join(request.scopes),
    }
    request.claims.update(kwargs)
    return common.generate_signed_token(
        settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"], request
    )
