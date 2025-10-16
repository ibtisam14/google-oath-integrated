from django.urls import path
from . import views

urlpatterns = [
    # Google OAuth
    path("auth/google/login/", views.google_login_redirect, name="google_login"),
    path("auth/google/callback/", views.google_callback, name="google_callback"),

    # GitHub OAuth
    path("auth/github/login/", views.github_login_redirect, name="github_login"),
    path("auth/github/callback/", views.github_callback, name="github_callback"),

    # Facebook OAuth
    path("auth/facebook/login/", views.facebook_login_redirect, name="facebook_login"),
    path("auth/facebook/callback/", views.facebook_callback, name="facebook_callback"),
]
