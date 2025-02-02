from django.urls import path
from .views import UserListView, CreateSuperUserView

app_name = "admin_api"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user_list"),
    path("create_superuser/", CreateSuperUserView.as_view(), name="create_superuser"),
]
