# myapp/middleware.py — upgrade your middleware

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from myapp.models import *

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        refresh = request.COOKIES.get('refresh_token')

        if token:
            try:
                decoded = AccessToken(token)
                user_id = decoded['user_id']
                request.user = CustomUserModel.objects.get(id=user_id)
            except TokenError:
                # Access token expired → try refresh automatically
                if refresh:
                    try:
                        new_refresh = RefreshToken(refresh)
                        new_access = str(new_refresh.access_token)

                        response = self.get_response(request)
                        # ✅ Set new access token cookie silently
                        response.set_cookie('access_token', new_access, httponly=True, samesite='Lax')
                        return response
                    except TokenError:
                        pass  # refresh also expired → user treated as logged out

        response = self.get_response(request)
        return response