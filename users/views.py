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
    REGISTRATION_SUCCESS,
    REGISTRATION_FAILED,
    PROFILE_UPDATE_SUCCESS,
    PROFILE_UPDATE_FAILED,
    USER_DELETED_SUCCESS,
    USER_NOT_FOUND,
    USER_DELETE_FAILED,
)
from .serializers import (
    ChangePasswordSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class LoginView(TokenObtainPairView):
    """Handle user login using JWT tokens."""

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for user login."""
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
    """Handle token refresh using refresh token."""

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for token refresh."""
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
    """Handle user logout by blacklisting the refresh token."""

    permission_classes = (AllowAny,)
    versioning_class = None  # Disable versioning for token endpoints

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for user logout."""
        try:
            response = super().post(request, *args, **kwargs)
            return api_response(message=LOGOUT_SUCCESS, status_code=status.HTTP_200_OK)
        except Exception as e:
            return api_response(
                message=LOGOUT_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class UserRegistrationView(APIView):
    """Handle user registration.

    Validates and creates a new user account with the provided email, password,
    first name and last name.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Process user registration request.

        Args:
            request: HTTP request object containing user registration data
            (email, password, confirm_password, first_name, last_name)
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return api_response(
                message=REGISTRATION_SUCCESS,
                data={
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            message=REGISTRATION_FAILED,
            error=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(APIView):
    """Handle changing the logged-in user's password.

    Requires authentication.
    Validates current password and ensures new password meets requirements.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for password change."""
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


class UserUpdateView(APIView):
    """Handle updating user profile information."""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def put(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle PUT request for user profile update."""
        try:
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                user = serializer.save()
                return api_response(
                    message=PROFILE_UPDATE_SUCCESS,
                    data={
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    status_code=status.HTTP_200_OK,
                )
            return api_response(
                message=PROFILE_UPDATE_FAILED,
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return api_response(
                message=PROFILE_UPDATE_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class UserDeleteView(APIView):
    """Handle soft delete of a user account."""

    permission_classes = (IsAuthenticated,)

    def delete(self, request: Any, user_id: int) -> Response:
        """Handle DELETE request for soft deleting a user."""
        try:
            user = request.user
            user.is_active = False  # Soft delete by setting is_active to False
            user.save()
            return api_response(
                message=USER_DELETED_SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return api_response(
                message=USER_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return api_response(
                message=USER_DELETE_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
