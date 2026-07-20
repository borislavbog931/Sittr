from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import SittrAuthenticationForm

urlpatterns = [
    path("signup/", views.signup_choice, name="signup_choice"),
    path("signup/owner/", views.signup_owner, name="signup_owner"),
    path("signup/caretaker/", views.signup_caretaker, name="signup_caretaker"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=SittrAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
