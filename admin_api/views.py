from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework import status
from utils.api import api_response
from utils.constants import (
    USER_RETRIEVE_SUCCESS,
    USER_RETRIEVE_FAILED,
)

User = get_user_model()


class UserListView(APIView):
    """View to list all users, accessible by admin only."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            users = User.objects.exclude(is_superuser=True).values(
                "id", "email", "first_name", "last_name"
            )
            return api_response(
                message=USER_RETRIEVE_SUCCESS,
                data=list(users),
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return api_response(
                message=USER_RETRIEVE_FAILED,
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
