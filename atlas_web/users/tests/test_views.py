import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import Client, RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from atlas_web.users.models import User
from atlas_web.users.tests.factories import UserFactory
from atlas_web.users.views import (
    UserDetailView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeDoneView,
    UserPasswordChangeView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    UserRedirectView,
    UserRegisterView,
    UserUpdateView,
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

pytestmark = pytest.mark.django_db


class TestUserRegisterView:
    def test_get_user_register_view(self, client: Client):
        response = client.get(reverse("users:register"))
        assertTemplateUsed(response, "users/register.html")

    def test_post_user_register_view_with_valid_data_redirects_to_user_detail_view(
        self, client: Client
    ):
        email = "cernetic@mpa-garching.mpg.de"
        data = {
            "email": email,
            "password1": "secretPass123",
            "password2": "secretPass123",
            "captcha_0": "dontcare",
            "captcha_1": "PASSED",  # CAPTCHA_TEST_MODE = True
        }

        response = client.post(reverse("users:register"), data=data)
        assert response.status_code == 302
        assert response.url == reverse("users:redirect")

        user = User.objects.filter(email=email)
        assert user.exists()
        user = user.first()
        assert type(user) == User

        # Follow redirect and expect a new user to exist, to be authenticated and logged in, and 302 to user_detail_view
        response = client.get(response.url)
        assert response.status_code == 302
        assert response.url == reverse("users:detail", kwargs={"pk": user.pk})

        # Finally, follow redirect to render user_detail_view
        response = client.get(response.url)
        assert response.status_code == 200
        assertTemplateUsed(response, "users/user_detail.html")


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/detail/{user.pk}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, pk=user.pk)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, pk=user.pk)

        assert response.status_code == 302
        assert response.url == "/users/login/?next=/fake-url/"


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/detail/{user.pk}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/detail/{user.pk}/"


class TestUserDetailView:
    @pytest.mark.skip(reason="Work in progress")
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, pk=user.pk)

        assert response.status_code == 200

    @pytest.mark.skip(reason="Work in progress")
    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, pk=user.pk)

        assert response.status_code == 403
        assert response.url == "/users/login/?next=/fake-url/"
