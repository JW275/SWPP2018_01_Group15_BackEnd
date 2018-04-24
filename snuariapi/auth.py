from snuariapi.models import *
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        cookie = request.COOKIES.get('auth')
        if not cookie:
            return None

        try:
            user = Token.objects.get(key=cookie).user
        except:
            return None
        return (user, None)
