from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from atlas_web.simulation.models import (
    AtlasSimulation,
    AtlasSimulationInput,
    AtlasSimulationOutput,
    AtlasSimulationSlurmJob,
)


class AtlasSimulationInputInline(admin.StackedInline):
    model = AtlasSimulationInput
    exclude = ("date_created", "date_updated", "last_updated_by")
    readonly_fields = ("folder",)
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AtlasSimulationSlurmJobInline(admin.StackedInline):
    model = AtlasSimulationSlurmJob
    exclude = ("date_created", "date_updated", "last_updated_by")
    readonly_fields = ("jobscript",)
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AtlasSimulationOutputInline(admin.StackedInline):
    model = AtlasSimulationOutput
    exclude = ("date_created", "date_updated", "last_updated_by")
    readonly_fields = ("folder",)
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AtlasSimulation)
class AtlasSimulationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "show_requested_by",
        "get_users_with_access_count",
        "get_slurmjob_status",
    ]
    search_fields = [
        "name",
        "requested_by__email",
        "requested_by__first_name",
        "requested_by__last_name",
    ]
    list_filter = ["requested_by", "slurmjob__status"]
    inlines = [
        AtlasSimulationInputInline,
        AtlasSimulationSlurmJobInline,
        AtlasSimulationOutputInline,
    ]
    filter_horizontal = [
        "access_list",
    ]
    readonly_fields = [
        "name",
        "date_created",
        "date_updated",
        "last_updated_by",
        "get_slurmjob_status",
    ]
    autocomplete_fields = ["requested_by"]

    fieldsets = (
        (None, {"fields": ("name", "requested_by", "access_list")}),
        (_("Meta"), {"fields": ("date_created", "date_updated", "last_updated_by")}),
    )

    def show_requested_by(self, obj):
        if not obj.requested_by:
            return "-"
        href = "<a href='{0}' alt='{1}'>{1}</a>".format(
            reverse(
                "admin:{0}_{1}_change".format(
                    obj.requested_by._meta.app_label, obj.requested_by._meta.model_name
                ),
                args=(obj.requested_by.id,),
            ),
            str(obj.requested_by),
        )
        return format_html(href)

    show_requested_by.short_description = _("Requested by")
    show_requested_by.admin_order_field = "requested_by"

    def get_users_with_access_count(self, obj):
        return obj.access_list.count()

    get_users_with_access_count.short_description = _("# users with access")
    get_users_with_access_count.admin_order_field = "access_list__count"

    def get_slurmjob_status(self, obj):
        return obj.slurmjob.get_status_display()

    get_slurmjob_status.short_description = _("Slurm Status")
    get_slurmjob_status.admin_order_field = "slurmjob__status"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# @admin.register(AtlasSimulationSlurmJob)
class AtlasSimulationSlurmJobAdmin(admin.ModelAdmin):
    list_display = [
        "simulation",
    ]
    search_fields = ["simulation"]
    readonly_fields = ["date_created", "date_updated", "last_updated_by"]

    fieldsets = (
        (None, {"fields": ("simulation",)}),
        (_("Meta"), {"fields": ("date_created", "date_updated", "last_updated_by")}),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# @admin.register(AtlasSimulationInput)
class AtlasSimulationInputAdmin(admin.ModelAdmin):
    list_display = [
        "simulation",
    ]
    search_fields = ["simulation"]
    readonly_fields = ["date_created", "date_updated", "last_updated_by"]

    fieldsets = (
        (None, {"fields": ("simulation",)}),
        (_("Meta"), {"fields": ("date_created", "date_updated", "last_updated_by")}),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# @admin.register(AtlasSimulationOutput)
class AtlasSimulationOutputAdmin(admin.ModelAdmin):
    list_display = [
        "simulation",
    ]
    search_fields = ["simulation"]
    readonly_fields = ["date_created", "date_updated", "last_updated_by"]

    fieldsets = (
        (None, {"fields": ("simulation",)}),
        (_("Meta"), {"fields": ("date_created", "date_updated", "last_updated_by")}),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()
