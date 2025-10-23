import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthEndpoints:
    # -----------------------
    # REGISTER TEST
    # -----------------------
    def test_register_user_successfully(self, client):
        """
        You must register a new user and return JWT tokens.
        """
        url = reverse("user-register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongPass123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "employee"
        }

        response = client.post(url, data, format="json")
        response_json = response.json()

        assert response.status_code == 201
        assert "tokens" in response_json
        assert "access" in response_json["tokens"]
        assert User.objects.filter(username="newuser").exists()

    # -----------------------
    # LOGIN TEST
    # -----------------------
    def test_login_user_and_get_tokens(self, client):
        """
        You must authenticate an existing user and return refresh and access tokens.
        """
        user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="testpass123",
            role="employee"
        )

        url = reverse("token_obtain_pair") 
        data = {"username": "loginuser", "password": "testpass123"}

        response = client.post(url, data, format="json")
        response_json = response.json()

        assert response.status_code == 200
        assert "refresh" in response_json
        assert "access" in response_json

    # -----------------------
    # REFRESH TOKEN TEST
    # -----------------------
    def test_refresh_token_returns_new_access(self, client):
        """
        You must generate a new access token when sending a valid refresh.
        """
        user = User.objects.create_user(
            username="refreshuser",
            email="refresh@example.com",
            password="refresh123",
            role="employee"
        )

        # Obtener token inicial
        token_url = reverse("token_obtain_pair")
        data = {"username": "refreshuser", "password": "refresh123"}
        res = client.post(token_url, data, format="json")
        refresh_token = res.json()["refresh"]

        # Refrescar token
        refresh_url = reverse("token_refresh")
        refresh_data = {"refresh": refresh_token}
        response = client.post(refresh_url, refresh_data, format="json")
        response_json = response.json()

        assert response.status_code == 200
        assert "access" in response_json
        assert isinstance(response_json["access"], str)
        assert len(response_json["access"]) > 10
