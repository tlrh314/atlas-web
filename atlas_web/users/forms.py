from captcha.fields import CaptchaField
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as DefaultPasswordResetForm
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(DefaultUserCreationForm):
    """ This form is used in the frontend, for public signup at the website """

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "captcha")

    def clean_email(self):
        super().clean()
        email = self.cleaned_data.get("email")
        existing_user = User.objects.filter(email=email)
        if existing_user.exists():  # Better to ask permission than forgiveness
            self.errors["email"] = ErrorList()
            self.errors["email"].append(
                "The chosen email address is already registered."
            )
        return email

    def save(self, commit=True):
        user = super().save()
        user.is_active = True
        user.is_validated = False
        user.save()

        subject = _(
            "Welcome to atlas-web. Your account is pending approval by our team."
        )
        context = {"user": str(user)}
        text_content = render_to_string("users/account_created.txt", context)
        html_content = render_to_string("users/account_created.html", context)
        user.send_email(subject, text_content, html_content)

        # TODO: push to Slack: "Hey admin, md5(user.email.lower()) signed up! Please verify/reject?
        return user


class UserPasswordResetForm(DefaultPasswordResetForm):
    """ This form is used in the frontend, for public signup at the website """

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "captcha")


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """ This form is used in the Django admin to change a user """

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """ This form is used in the Django admin to create a user """

    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email address has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        exclude = ("username",)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:  # Better to ask forgiveness than permission
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])
