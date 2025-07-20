from django.urls import path
from django.contrib.auth.views import LogoutView


from .views import (
    home_view,
    login_view,
    signup_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
