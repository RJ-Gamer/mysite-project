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
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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


class CreateSuperUserView(View):
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists."}, status=400)

        user = User.objects.create_superuser(
            username=username, email=email, password=password
        )

        return JsonResponse(
            {"message": "Superuser created successfully.", "user_id": user.id},
            status=201,
        )
