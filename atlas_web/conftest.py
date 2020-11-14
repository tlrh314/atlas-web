"""
Note that the conftest makes various things available to the test runner.  For example, most TestCases
need a user, so a new user is conveniently generated using the UserFactory.
"""

import pytest

from atlas_web.users.models import User
from atlas_web.users.tests.factories import AdminFactory, UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def admin() -> User:
    admin = AdminFactory()
    admin.set_password("admin_password")
    admin.save()
    return admin
