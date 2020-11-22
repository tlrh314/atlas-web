from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import ClockedSchedule, IntervalSchedule, SolarSchedule

from atlas_web.users.forms import (
    UserAdminChangeForm,
    UserAdminCreationForm,
    UserPasswordResetForm,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    ordering = ["-pk"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_validated",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["is_active", "is_validated", "is_staff", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    actions = ["validate_user", "send_password_reset"]

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields = ["last_login", "date_created", "last_updated_by"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_validated",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                )
            },
        ),
        (_("Meta"), {"fields": ("last_login", "date_created", "last_updated_by")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def validate_user(self, request, queryset):
        already_validated = 0
        newly_validated = 0
        subject = _("Your account at atlas-web has been approved")
        for user in queryset.iterator():
            if user.is_validated:
                already_validated += 1
                continue  # don't want to send email twice

            context = {"user": str(user)}
            text_content = render_to_string("users/account_approved.txt", context)
            html_content = render_to_string("users/account_approved.html", context)
            user.send_email(subject, text_content, html_content)
            newly_validated += 1

        # After sending the mail we proceed to send the account approval mail
        queryset.update(is_active=True)
        queryset.update(is_validated=True)
        self.message_user(
            request,
            _(
                "Succesfully validated {} users, and skipped {} b/c already validated.".format(
                    newly_validated, already_validated
                )
            ),
        )

    validate_user.short_description = _(
        "Mark users as validated and send an automated welcome email to inform them."
    )

    def send_password_reset(self, request, queryset):
        for user in queryset:
            try:
                validate_email(user.email)
                form = UserPasswordResetForm(data={"email": user.email})
                form.is_valid()

                form.save(
                    email_template_name="users/password_forced_reset_email.html",
                    extra_email_context={"full_name": user.get_full_name()},
                )
                self.message_user(request, _("Succesfully sent password reset email."))
            except ValidationError:
                self.message_user(
                    request,
                    _("User does not have a valid email address"),
                    level="error",
                )

    send_password_reset.short_description = _("Send password reset link")


# We hide the this Site thingy from Django's Sites framework b/c it'll be confusing
# for the atlas-web admins. However, we cannot simply remove the app b/c underlying
# packages rely on django.contrib.sites to sit in the INSTALLED_APPS, unfortunately.
admin.site.unregister(Site)

# We will most likely not use the Group functionality, so let just hide this too.
admin.site.unregister(Group)

admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
