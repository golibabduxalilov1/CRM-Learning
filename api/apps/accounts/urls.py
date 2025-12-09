from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("otp/verify/", views.verify_otp, name="verify_otp"),
    path("logout/", views.logout, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.current_user, name="current_user"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "allowlist/", views.AllowedEmailListCreateView.as_view(), name="allowlist-list"
    ),
    path(
        "allowlist/<int:pk>/",
        views.AllowedEmailDestroyView.as_view(),
        name="allowlist-delete",
    ),
    path("users/<str:role>/", views.UserListView.as_view(), name="users-by-role"),
    path("users/", views.UserListView.as_view(), name="users-list"),
]
