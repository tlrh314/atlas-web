from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    @post_generation
    def first_name(self, create: bool, extracted: Sequence[Any], **kwargs):
        self.first_name = "Test: {}".format(self.first_name)

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)


class AdminFactory(UserFactory):
    is_active = True
    is_validated = True
    is_staff = True
    is_superuser = True
