import re
from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils.constants import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_REQUIREMENTS,
    PASSWORD_MISMATCH,
    CURRENT_PASSWORD_INCORRECT,
    CURRENT_PASSWORD_LABEL,
    NEW_PASSWORD_LABEL,
    CONFIRM_PASSWORD_LABEL,
)

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.

    Validates that:
    1. Current password is correct
    2. New password meets complexity requirements
    3. New password and confirmation match

    Fields:
        current_password: User's current password for verification
        new_password: New password that meets complexity requirements
        confirm_password: Must match new_password
    """

    current_password = serializers.CharField(
        label=CURRENT_PASSWORD_LABEL,
        style={"input_type": "password"},
        write_only=True,
    )
    new_password = serializers.CharField(
        label=NEW_PASSWORD_LABEL,
        style={"input_type": "password"},
        write_only=True,
    )
    confirm_password = serializers.CharField(
        label=CONFIRM_PASSWORD_LABEL,
        style={"input_type": "password"},
        write_only=True,
    )

    def validate_current_password(self, value: str) -> str:
        """
        Validate that the current password is correct.

        Args:
            value: The current password provided by the user

        Returns:
            str: The validated current password

        Raises:
            serializers.ValidationError: If the current password is incorrect
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(CURRENT_PASSWORD_INCORRECT)
        return value

    def validate_new_password(self, value: str) -> str:
        """
        Validate that the new password meets complexity requirements.

        Password must:
        1. Be at least 8 characters long
        2. Contain at least one uppercase letter
        3. Contain at least one lowercase letter
        4. Contain at least one number
        5. Contain at least one special character

        Args:
            value: The new password to validate

        Returns:
            str: The validated new password

        Raises:
            serializers.ValidationError: If the password doesn't meet requirements
        """
        if len(value) < 8:
            raise serializers.ValidationError(PASSWORD_MIN_LENGTH)

        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            value,
        ):
            raise serializers.ValidationError(PASSWORD_REQUIREMENTS)

        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that new_password and confirm_password match.

        Args:
            data: Dictionary containing the serializer fields

        Returns:
            Dict[str, Any]: The validated data

        Raises:
            serializers.ValidationError: If passwords don't match
        """
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": PASSWORD_MISMATCH})
        return data

    def save(self, **kwargs: Any) -> User:
        """
        Save the new password for the user.

        Returns:
            User: The updated user instance

        Side Effects:
            - Sets the user's password to the new password
            - Saves the user instance
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
