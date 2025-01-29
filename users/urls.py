from django.urls import path
from .views import LoginView, RefreshTokenView, LogoutView, ChangePasswordView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
