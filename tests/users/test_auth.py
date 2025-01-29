import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.factories import UserFactory
from utils.constants import (
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_CHANGE_FAILED,
    PASSWORD_MISMATCH,
    CURRENT_PASSWORD_INCORRECT,
    PASSWORD_MIN_LENGTH,
    PASSWORD_REQUIREMENTS,
    REGISTRATION_SUCCESS,
    REGISTRATION_FAILED,
    EMAIL_EXISTS,
    PROFILE_UPDATE_SUCCESS,
    PROFILE_UPDATE_FAILED,
    EMAIL_CHANGE_NOT_ALLOWED,
)


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, user):
        response = api_client.post(
            reverse("users:login", kwargs={"version": "v1"}),
            data={
                "email": user.email,
                "password": "testpass123",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == LOGIN_SUCCESS
        assert "access" in response_data["data"]
        assert "refresh" in response_data["data"]

    def test_login_invalid_credentials(self, api_client, user):
        response = api_client.post(
            reverse("users:login", kwargs={"version": "v1"}),
            data={
                "email": user.email,
                "password": "wrongpassword",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == LOGIN_FAILED


@pytest.mark.django_db
class TestChangePasswordView:
    def test_change_password_success(self, authenticated_client):
        response = authenticated_client.post(
            reverse("users:change_password", kwargs={"version": "v1"}),
            data={
                "current_password": "testpass123",
                "new_password": "NewPass@123",
                "confirm_password": "NewPass@123",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == PASSWORD_CHANGE_SUCCESS

    def test_change_password_wrong_current_password(self, authenticated_client):
        response = authenticated_client.post(
            reverse("users:change_password", kwargs={"version": "v1"}),
            data={
                "current_password": "wrongpassword",
                "new_password": "NewPass@123",
                "confirm_password": "NewPass@123",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED
        assert CURRENT_PASSWORD_INCORRECT in str(response_data["error"])

    def test_change_password_mismatch(self, authenticated_client):
        response = authenticated_client.post(
            reverse("users:change_password", kwargs={"version": "v1"}),
            data={
                "current_password": "testpass123",
                "new_password": "NewPass@123",
                "confirm_password": "DifferentPass@123",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED
        assert PASSWORD_MISMATCH in str(response_data["error"])

    def test_change_password_weak_password(self, authenticated_client):
        response = authenticated_client.post(
            reverse("users:change_password", kwargs={"version": "v1"}),
            data={
                "current_password": "testpass123",
                "new_password": "weak",
                "confirm_password": "weak",
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == PASSWORD_CHANGE_FAILED
        assert PASSWORD_MIN_LENGTH in str(response_data["error"]["new_password"])

    def test_change_password_unauthenticated(self, api_client):
        response = api_client.post(
            reverse("users:change_password", kwargs={"version": "v1"}),
            data={
                "current_password": "testpass123",
                "new_password": "NewPass@123",
                "confirm_password": "NewPass@123",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserRegistrationView:
    """Test cases for user registration endpoint."""

    def test_registration_success(self, api_client: APIClient) -> None:
        """Test successful user registration."""
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(
            reverse("users:register", kwargs={"version": "v1"}), data
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data["message"] == REGISTRATION_SUCCESS
        assert response_data["data"]["email"] == data["email"]
        assert response_data["data"]["first_name"] == data["first_name"]
        assert response_data["data"]["last_name"] == data["last_name"]

    def test_registration_email_exists(self, api_client: APIClient) -> None:
        """Test registration with existing email."""
        user = UserFactory()
        data = {
            "email": user.email,
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(
            reverse("users:register", kwargs={"version": "v1"}), data
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == REGISTRATION_FAILED
        assert "User with this Email address already exists." in str(
            response_data["error"]["email"]
        )

    def test_registration_password_mismatch(self, api_client: APIClient) -> None:
        """Test registration with mismatched passwords."""
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@1234",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(
            reverse("users:register", kwargs={"version": "v1"}), data
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == REGISTRATION_FAILED
        assert PASSWORD_MISMATCH in str(response_data["error"]["confirm_password"])

    def test_registration_weak_password(self, api_client: APIClient) -> None:
        """Test registration with weak password."""
        data = {
            "email": "test@example.com",
            "password": "weakpass",
            "confirm_password": "weakpass",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(
            reverse("users:register", kwargs={"version": "v1"}), data
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == REGISTRATION_FAILED
        assert PASSWORD_REQUIREMENTS in str(response_data["error"]["password"])

    def test_registration_missing_fields(self, api_client: APIClient) -> None:
        """Test registration with missing required fields."""
        data = {
            "email": "test@example.com",
            "password": "Test@123",
        }
        response = api_client.post(
            reverse("users:register", kwargs={"version": "v1"}), data
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data["message"] == REGISTRATION_FAILED
        assert "confirm_password" in response_data["error"]


@pytest.mark.django_db
class TestUserUpdateView:
    """Test cases for user profile update endpoint."""

    def test_profile_update_success(self, authenticated_client):
        """Test successful profile update."""
        data = {"first_name": "Updated", "last_name": "Name"}
        response = authenticated_client.put(
            "/api/v1/auth/profile/", json.dumps(data), content_type="application/json"
        )
        response_data = response.json()
        print("Response data:", response_data)  # Print response data for debugging
        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == PROFILE_UPDATE_SUCCESS
        assert response_data["data"]["first_name"] == data["first_name"]
        assert response_data["data"]["last_name"] == data["last_name"]

    def test_profile_update_email_change_attempt(self, authenticated_client, user):
        """Test that email cannot be changed."""
        original_email = user.email
        data = {
            "email": "newemail@example.com",
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = authenticated_client.put(
            "/api/v1/auth/profile/", json.dumps(data), content_type="application/json"
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == PROFILE_UPDATE_SUCCESS
        assert (
            response_data["data"]["email"] == original_email
        )  # Email should remain unchanged
        assert response_data["data"]["first_name"] == data["first_name"]
        assert response_data["data"]["last_name"] == data["last_name"]

    def test_profile_update_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot update profile."""
        data = {"first_name": "Updated", "last_name": "Name"}
        response = api_client.put(
            "/api/v1/auth/profile/", json.dumps(data), content_type="application/json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_update_partial(self, authenticated_client, user):
        """Test partial profile update."""
        original_last_name = user.last_name
        data = {"first_name": "UpdatedFirst"}
        response = authenticated_client.put(
            "/api/v1/auth/profile/", json.dumps(data), content_type="application/json"
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data["message"] == PROFILE_UPDATE_SUCCESS
        assert response_data["data"]["first_name"] == data["first_name"]
        assert (
            response_data["data"]["last_name"] == original_last_name
        )  # Should remain unchanged
