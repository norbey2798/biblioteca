from django.urls import path
from .views import login_view, logout_view, construction_view, register_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("construction/", construction_view, name="construction"),
    path("register/", register_view, name="register"),
]
