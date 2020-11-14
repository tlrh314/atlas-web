from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from atlas_web.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    ordering = ["-pk"]
    list_display = ["email", "first_name", "last_name", "is_superuser", "is_validated"]
    search_fields = ["email", "first_name", "last_name"]
    actions = ["validate_user"]

    fieldsets = (("User", {"fields": ("",)}),) + tuple(auth_admin.UserAdmin.fieldsets)
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

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
