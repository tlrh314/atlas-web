from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

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
                    "groups",
                    "user_permissions",
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
        queryset.update(is_validated=True)
        subject = _("Your account at atlas-web has been approved")
        for user in queryset.iterator():
            context = {"user": str(user)}
            text_content = render_to_string("users/account_approved.txt", context)
            html_content = render_to_string("users/account_approved.html", context)
            user.send_email(subject, text_content, html_content)

    validate_user.short_description = _(
        "Mark users as validated send an automated email to inform them."
    )


admin.site.unregister(Group)
