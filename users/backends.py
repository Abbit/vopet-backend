from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .utils import get_token_from_request, get_user_by_token

User = get_user_model()


class JWTBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        token = get_token_from_request(request)

        if token is not None:
            return get_user_by_token(token)

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
