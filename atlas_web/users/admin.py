from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import ClockedSchedule, IntervalSchedule, SolarSchedule

from atlas_web.users.forms import UserAdminChangeForm, UserAdminCreationForm

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
    actions = ["validate_user"]

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

    def validate_user(modeladmin, request, queryset):
        subject = _("Your account at atlas-web has been approved")
        for user in queryset.iterator():
            if user.is_validated:
                continue  # don't want to send email twice

            context = {"user": str(user)}
            text_content = render_to_string("users/account_approved.txt", context)
            html_content = render_to_string("users/account_approved.html", context)
            user.send_email(subject, text_content, html_content)

        # After sending the mail we proceed to send the account approval mail
        queryset.update(is_active=True)
        queryset.update(is_validated=True)

    validate_user.short_description = _(
        "Mark users as validated and send an automated welcome email to inform them."
    )


# We hide the this Site thingy from Django's Sites framework b/c it'll be confusing
# for the atlas-web admins. However, we cannot simply remove the app b/c underlying
# packages rely on django.contrib.sites to sit in the INSTALLED_APPS, unfortunately.
admin.site.unregister(Site)

# We will most likely not use the Group functionality, so let just hide this too.
admin.site.unregister(Group)

admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
