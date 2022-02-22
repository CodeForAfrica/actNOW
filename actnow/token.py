import json

from oauth2_provider.models import get_access_token_model
from oauth2_provider.views import TokenView as OAuth2TokenView


class TokenView(OAuth2TokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        body = json.loads(response.content)
        access_token = body.get("access_token")
        token = get_access_token_model().objects.get(token=access_token)
        body["user"] = {
            "id": token.user.id,
            "profile_id": token.user.userprofile.id,
            "email": token.user.email,
            "username": token.user.username,
        }
        response.content = json.dumps(body)
        return response
