from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core_auth.factory import AuthenticatorFactory

from rest_framework import generics
from .models import CustomUser
from .serializers import SignUpSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        auth_type = request.data.get('auth_type', 'default')
        authenticator = AuthenticatorFactory.get_authenticator(auth_type)

        user = authenticator.authenticate(request)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer