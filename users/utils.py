import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from .exceptions import AuthError

jwt_secret = settings.JWT_SECRET_KEY
token_prefix = "Bearer"


def get_token_from_request(request):
    auth_header = request.headers.get("Authorization", "").split()

    if len(auth_header) != 2 or auth_header[0].lower() != token_prefix.lower():
        return None
    return auth_header[1]


def create_token(user):
    return jwt.encode(
        {"username": user.username}, jwt_secret, algorithm="HS256",
    ).decode("utf-8")


def get_token_payload(token):
    return jwt.decode(token, jwt_secret, algorithms=["HS256"])


def get_user_by_token(token):
    UserModel = get_user_model()

    payload = get_token_payload(token)

    if not payload["username"]:
        raise AuthError("Invalid payload")

    try:
        user = UserModel.objects.get(username=payload["username"])
    except UserModel.DoesNotExist:
        user = None

    return user
