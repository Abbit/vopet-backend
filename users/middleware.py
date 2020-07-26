from django.contrib.auth import authenticate
from .utils import get_token_from_request


def _authenticate(request):
    is_anonymous = not hasattr(request, "user") or request.user.is_anonymous
    return is_anonymous and get_token_from_request(request) is not None


class JWTMiddleware:
    def resolve(self, next, root, info, **kwargs):
        context = info.context

        if _authenticate(context):
            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

        return next(root, info, **kwargs)
