from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from company.models import Company

User = get_user_model()


def create_user_with_role(
        username: str, 
        email: str, 
        password: str, 
        first_name: str, 
        last_name: str, 
        role: str,
        company : Company,
        ):
    """
    Create a new user with the specified role and securely hashed password.

    Args:
        username (str): The username for the new user.
        email (str): The user's email address.
        password (str): The user's plain-text password (will be hashed).
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        role (str): The role assigned to the user.
        company : (Company) : The compoany assigned to the user.

    Returns:
        User: The created user instance.
    """
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
        company=company,
    )
    user.set_password(password)
    user.save()
    return user


def generate_jwt_for_user(user):
    """
    Generate JWT authentication tokens (access and refresh) for a given user.

    Args:
        user (User): The user instance for which to generate tokens.

    Returns:
        dict: A dictionary containing 'refresh' and 'access' JWT tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
