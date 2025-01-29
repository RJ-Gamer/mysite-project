import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
