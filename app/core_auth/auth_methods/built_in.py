from django.contrib.auth import authenticate
from core_auth.auth_methods.base import BaseAuthenticator

class BuiltInAuthenticator(BaseAuthenticator):
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        return user