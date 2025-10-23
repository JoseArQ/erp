from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    """
    API view for registering new users and returning JWT tokens.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

