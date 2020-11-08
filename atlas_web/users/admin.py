from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from atlas_web.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "name", "is_superuser", "is_validated"]
    search_fields = ["name"]
    actions = ["validate_user"]

    def validate_user(modeladmin, request, queryset):
        print("validating_users")
        queryset.update(is_validated=True)

    validate_user.short_description = "Mark users as validated."
