from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model

from common.responses import responses

from company.services import get_company

from .serializers import UserRegisterSerializer
from . import services as user_services

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    """
    API view for registering new users and returning JWT tokens.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration logic:
        - Validate input data
        - Retrieve company (and entity if needed)
        - Create user via service
        - Return JWT tokens
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        company_id = validated_data["company_id"]
        company = get_company({"id": company_id})

       
        user = user_services.create_user_with_role(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            company=company,
        )

        tokens = user_services.generate_jwt_for_user(user)

        return responses.success_response(
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "company": {
                    "id": company.id, 
                    "name": company.name,
                    },
                "tokens": tokens,
            }, 
            status_code=status.HTTP_201_CREATED,
            )
