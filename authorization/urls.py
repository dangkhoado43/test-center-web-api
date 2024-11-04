from django.urls import path
from .views import LoginView, LogoutView, CustomTokenRefreshView, RevokeTokenView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # User login
    path('logout/', LogoutView.as_view(), name='logout'),  # User logout
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/revoke/', RevokeTokenView.as_view(), name='token_revoke'),  # Revoke token
]
