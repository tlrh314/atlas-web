import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from atlas_web.users.admin import UserAdmin

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestUserAdmin:
    def test_admin_action_validate_user(self, admin: User, client: Client):

        # Make sure we have a User instance that is admin (to be allowed to
        # run the admin action), but that admin happends to be non-validated.
        # So the admin calls the admin action to validate_user on themselves.
        admin.is_validated = False
        admin.save()
        assert not admin.is_validated

        # Use the admin account to login so it has access to the admin
        assert client.login(email=admin.email, password="admin_password")

        # Check that there are no emails because we expect the admin action
        # to send an email
        assert len(mail.outbox) == 0

        url = reverse("admin:users_user_changelist")
        assert url == "/admin/users/user/"

        queryset = User.objects.values_list("pk", flat=True)
        data = {"action": "validate_user", "_selected_action": queryset}
        response = client.post(url, data, follow=True)
        assert response.status_code == 200

        admin.refresh_from_db(fields=["is_active", "is_validated"])
        assert admin.is_active
        assert admin.is_validated

        assert not User.objects.filter(
            is_validated=False, pk__in=data["_selected_action"]
        ).exists()
        assert (
            User.objects.filter(
                is_validated=True, pk__in=data["_selected_action"]
            ).count()
            == queryset.count()
        )

        assert len(mail.outbox) == queryset.count()
        subject = _("Your account at atlas-web has been approved")
        assert mail.outbox[0].subject == subject

    def test_admin_action_validate_user_does_not_email_twice(
        self, admin: User, client: Client
    ):
        assert admin.is_validated
        assert client.login(email=admin.email, password="admin_password")
        url = reverse("admin:users_user_changelist")
        queryset = User.objects.values_list("pk", flat=True)
        data = {"action": "validate_user", "_selected_action": queryset}
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert not len(mail.outbox)

    def test_admin_form_save_updates_last_updated_by(
        self, admin: User, rf: RequestFactory
    ):
        assert not admin.last_updated_by

        url = reverse("admin:users_user_change", args=[admin.pk])
        assert url == "/admin/users/user/{}/change/".format(admin.pk)

        request = rf.get(url)
        request.user = admin

        user_admin = UserAdmin(model=User, admin_site=AdminSite())
        user_admin.save_model(obj=admin, request=request, form=None, change=None)

        admin.refresh_from_db(fields=["last_updated_by"])
        assert admin.last_updated_by.pk == admin.pk
