from rest_framework import generics, authentication, permissions
from accounts.serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system, RegisterView"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
