from django.urls import path
from .views import (
    Login, Register, ChangePassword, RetrieveUpdateDestroyAccount,
)

app_name = "users"

urlpatterns = [
    path("login/", Login.as_view(), name="Login"),
    path("register/", Register.as_view(), name="Register"),

    path("password/change/", ChangePassword.as_view(), name="ChangePassword"),

    path("update/<int:pk>/",
         RetrieveUpdateDestroyAccount.as_view(), name="RetrieveUpdateDestroyAccount"),
]
