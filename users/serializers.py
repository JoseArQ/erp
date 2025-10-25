from rest_framework import serializers
from django.contrib.auth import get_user_model
from .enums import UserRole

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with role and returning JWT tokens.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=UserRole.choices(), default=UserRole.EMPLOYEE.value)
    tokens = serializers.SerializerMethodField(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        """
        Meta configuration for the UserRegisterSerializer.
        """
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'password', 
            'first_name', 
            'last_name', 
            'role', 
            'tokens',
            "company_id",
            ]
        