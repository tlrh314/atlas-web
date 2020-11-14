from django.urls import path

from atlas_web.users.views import (
    user_detail_view,
    user_login_view,
    user_logout_view,
    user_password_change,
    user_password_change_done,
    user_password_reset,
    user_password_reset_complete,
    user_password_reset_confirm,
    user_password_reset_done,
    user_redirect_view,
    user_register_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("register/", user_register_view, name="register"),
    path("login/", user_login_view, name="login"),
    path("logout/", user_logout_view, name="logout"),
    path("redirect/", view=user_redirect_view, name="redirect"),
    path("update/", view=user_update_view, name="update"),
    path("<str:pk>/", view=user_detail_view, name="detail"),
    path("password_change/", user_password_change, name="password_change"),
    path(
        "password_change/done/",
        user_password_change_done,
        name="password_change_done",
    ),
    path(
        "password_reset/",
        user_password_reset,
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        user_password_reset_done,
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        user_password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        user_password_reset_complete,
        name="password_reset_complete",
    ),
]
