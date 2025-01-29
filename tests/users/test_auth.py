import pytest
from django.urls import reverse
from rest_framework import status
from utils.constants import (
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_CHANGE_FAILED,
    PASSWORD_MISMATCH,
    CURRENT_PASSWORD_INCORRECT,
)


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, user):
        url = "/api/v1/auth/login/"
        data = {
            "email": user.email,
            "password": "testpass123",
        }

        response = api_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == LOGIN_SUCCESS
        assert "access" in response_data["data"]
        assert "refresh" in response_data["data"]

    def test_login_invalid_credentials(self, api_client, user):
        url = "/api/v1/auth/login/"
        data = {
            "email": user.email,
            "password": "wrongpassword",
        }

        response = api_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == LOGIN_FAILED


@pytest.mark.django_db
class TestChangePasswordView:
    def test_change_password_success(self, authenticated_client):
        url = "/api/v1/auth/change-password/"
        data = {
            "current_password": "testpass123",
            "new_password": "NewPass@123",
            "confirm_password": "NewPass@123",
        }

        response = authenticated_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == PASSWORD_CHANGE_SUCCESS

    def test_change_password_wrong_current_password(self, authenticated_client):
        url = "/api/v1/auth/change-password/"
        data = {
            "current_password": "wrongpassword",
            "new_password": "NewPass@123",
            "confirm_password": "NewPass@123",
        }

        response = authenticated_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED
        assert CURRENT_PASSWORD_INCORRECT in str(response_data["error"])

    def test_change_password_mismatch(self, authenticated_client):
        url = "/api/v1/auth/change-password/"
        data = {
            "current_password": "testpass123",
            "new_password": "NewPass@123",
            "confirm_password": "DifferentPass@123",
        }

        response = authenticated_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED
        assert PASSWORD_MISMATCH in str(response_data["error"])

    def test_change_password_weak_password(self, authenticated_client):
        url = "/api/v1/auth/change-password/"
        data = {
            "current_password": "testpass123",
            "new_password": "weak",
            "confirm_password": "weak",
        }

        response = authenticated_client.post(url, data)
        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED

    def test_change_password_unauthenticated(self, api_client):
        url = "/api/v1/auth/change-password/"
        data = {
            "current_password": "testpass123",
            "new_password": "NewPass@123",
            "confirm_password": "NewPass@123",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
