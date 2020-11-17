import pytest
from django.contrib.auth import get_user_model

from atlas_web.users.forms import UserCreationForm
from atlas_web.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestUserCreationForm:
    def test_clean_email(self):
        assert User.objects.count() == 0
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "email": proto_user.email,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert form.is_valid()
        assert form.clean_email() == proto_user.email

        # Creating a user, which should result in an active, but non-validated user
        user = form.save()
        assert user.email == proto_user.email
        assert User.objects.count() == 1

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "email": proto_user.email,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
