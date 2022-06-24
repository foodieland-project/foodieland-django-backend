from rest_framework import generics, authentication, permissions
from .serializers import AuthTokenSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system, RegisterView"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES