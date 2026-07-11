"""
Accounts URL patterns
"""
from django.urls import include, path
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Email verification
    path(
        "verify/<uidb64>/<token>/",
        views.EmailVerificationView.as_view(),
        name="verify_email",
    ),

    # User settings
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path(
        "settings/change-password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),

    # Profile
    path("profile/", views.ProfileRedirectView.as_view(), name="profile_redirect"),

    # Social authentication (Google, GitHub, LinkedIn)
    path("social/", include("allauth.socialaccount.urls")),
]