from django.shortcuts import render
from typing import Any
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from django.contrib.auth import get_user_model
from utils.api import api_response
from utils.constants import (
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    TOKEN_REFRESH_SUCCESS,
    TOKEN_REFRESH_FAILED,
    LOGOUT_SUCCESS,
    LOGOUT_FAILED,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_CHANGE_FAILED,
)
from .serializers import ChangePasswordSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    """
    View for user login using JWT tokens.

    Returns:
        On success:
        {
            "message": "Login successful",
            "status_code": 200,
            "error": null,
            "data": {
                "access": "<access_token>",
                "refresh": "<refresh_token>"
            }
        }

        On failure:
        {
            "message": "Login failed",
            "status_code": 400,
            "error": "<error_message>",
            "data": null
        }
    """

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST request for user login.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: API response with tokens or error message
        """
        try:
            response = super().post(request, *args, **kwargs)
            return api_response(
                data=response.data,
                message=LOGIN_SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return api_response(
                message=LOGIN_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class RefreshTokenView(TokenRefreshView):
    """
    View for refreshing expired access tokens using refresh token.

    Returns:
        On success:
        {
            "message": "Token refresh successful",
            "status_code": 200,
            "error": null,
            "data": {
                "access": "<new_access_token>"
            }
        }

        On failure:
        {
            "message": "Token refresh failed",
            "status_code": 400,
            "error": "<error_message>",
            "data": null
        }
    """

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST request for token refresh.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: API response with new access token or error message
        """
        try:
            response = super().post(request, *args, **kwargs)
            return api_response(
                data=response.data,
                message=TOKEN_REFRESH_SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return api_response(
                message=TOKEN_REFRESH_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(TokenBlacklistView):
    """
    View for user logout by blacklisting the refresh token.

    Returns:
        On success:
        {
            "message": "Logout successful",
            "status_code": 200,
            "error": null,
            "data": null
        }

        On failure:
        {
            "message": "Logout failed",
            "status_code": 400,
            "error": "<error_message>",
            "data": null
        }
    """

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST request for user logout.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: API response indicating logout status
        """
        try:
            response = super().post(request, *args, **kwargs)
            return api_response(message=LOGOUT_SUCCESS, status_code=status.HTTP_200_OK)
        except Exception as e:
            return api_response(
                message=LOGOUT_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordView(APIView):
    """
    View for changing the logged-in user's password.

    Requires authentication.
    Validates current password and ensures new password meets requirements.

    Returns:
        On success:
        {
            "message": "Password changed successfully",
            "status_code": 200,
            "error": null,
            "data": null
        }

        On failure:
        {
            "message": "Failed to change password",
            "status_code": 400,
            "error": {
                "current_password": ["Current password is incorrect"],
                "new_password": ["Password must be at least 8 characters long"],
                "confirm_password": ["Passwords do not match"]
            },
            "data": null
        }
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST request for password change.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: API response indicating password change status
        """
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return api_response(
                    message=PASSWORD_CHANGE_SUCCESS,
                    status_code=status.HTTP_200_OK,
                )
            return api_response(
                message=PASSWORD_CHANGE_FAILED,
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return api_response(
                message=PASSWORD_CHANGE_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
