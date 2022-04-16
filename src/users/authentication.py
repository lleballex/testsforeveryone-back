from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

from .models import User
from .utils import decode_auth_token


class Authentication(BaseAuthentication):
    """Authenticates if headers have auth token"""

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTH_TOKEN')

        if not token: return None

        user_id = decode_auth_token(token)

        if not user_id:
            raise AuthenticationFailed('Token is invalid')

        try:
            return (User.objects.get(id=user_id), None)
        except User.DoesNotExist:
            raise AuthenticationFailed('Token is invalid')