from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .enums import UserRole
from . import services

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with role and returning JWT tokens.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=UserRole.choices(), default=UserRole.EMPLOYEE.value)
    tokens = serializers.SerializerMethodField(read_only=True)

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
            ]
        
        def create(self, validated_data):
            """
            Create a new user using the provided validated data.

            Args:
                validated_data (dict): Data validated by the serializer.

            Returns:
                User: The newly created user instance.
            """
            user = services.create_user_with_role(**validated_data)
            return user

        def get_tokens(self, obj):
            """
            Retrieve JWT tokens for the created user.

            Args:
                obj (User): The user instance.

            Returns:
                dict: A dictionary containing 'refresh' and 'access' tokens.
            """
            return services.generate_jwt_for_user(obj)
