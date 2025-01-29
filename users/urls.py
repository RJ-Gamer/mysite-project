from django.urls import path
from .views import (
    LoginView,
    RefreshTokenView,
    LogoutView,
    ChangePasswordView,
    UserRegistrationView,
    UserUpdateView,
    UserDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserUpdateView.as_view(), name='profile_update'),
    path('delete/<int:user_id>/', UserDeleteView.as_view(), name='user_delete'),
]
