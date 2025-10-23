import pytest
from django.contrib.auth import get_user_model
from users.services import create_user_with_role, generate_jwt_for_user

User = get_user_model()


@pytest.mark.django_db
def test_create_user_with_role_creates_user_correctly():
    """Debe crear un usuario con rol y contraseña encriptada."""
    user = create_user_with_role(
        username="testuser",
        email="test@example.com",
        password="securePass123",
        first_name="Test",
        last_name="User",
        role="employee",
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "employee"
    assert user.check_password("securePass123") 
    assert user.id is not None  


@pytest.mark.django_db
def test_generate_jwt_for_user_returns_valid_tokens():
    """Debe generar tokens JWT válidos (refresh y access)."""
    user = User.objects.create_user(
        username="tokenuser",
        email="token@example.com",
        password="superpass123",
        role="employee"
    )

    tokens = generate_jwt_for_user(user)

    assert "refresh" in tokens
    assert "access" in tokens
    assert isinstance(tokens["refresh"], str)
    assert isinstance(tokens["access"], str)
    assert len(tokens["access"]) > 10 