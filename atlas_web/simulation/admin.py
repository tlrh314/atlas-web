from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from atlas_web.simulation.models import (
    AtlasSimulation,
    AtlasSimulationInput,
    AtlasSimulationOutput,
    AtlasSimulationSlurmJob,
)


# TODO: @Miha, you can also try what it looks like when you inherit from admin.StackedInline
class AtlasSimulationInputInline(admin.TabularInline):
    model = AtlasSimulationInput
    exclude = ("date_created", "date_updated", "last_updated_by")
    # TODO: @Miha, you can also try what it looks like when you set extra = 0, or extra = 2
    extra = 1


class AtlasSimulationSlurmJobInline(admin.TabularInline):
    model = AtlasSimulationSlurmJob
    exclude = ("date_created", "date_updated", "last_updated_by")
    extra = 1


class AtlasSimulationOutputInline(admin.TabularInline):
    model = AtlasSimulationOutput
    exclude = ("date_created", "date_updated", "last_updated_by")
    extra = 1


@admin.register(AtlasSimulation)
class AtlasSimulationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = ["name"]
    inlines = [
        AtlasSimulationInputInline,
        AtlasSimulationSlurmJobInline,
        AtlasSimulationOutputInline,
    ]
    readonly_fields = ["date_created", "date_updated", "last_updated_by"]

    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Meta"), {"fields": ("date_created", "date_updated", "last_updated_by")}),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# TODO: @Miha, I've now not registered the related model instances individually
# because it's clearer if they're just inline in the AtlasSimulationAdmin.
# But if you do want to show the admin for these model instances, then you can
# uncomment the line as to register the admins implemented below.
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
