from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AtlasSimulation(models.Model):
    # TODO: @Miha, one way of namespacing simulation folders that I often use
    # is /w unix timestamp. Then we enforce unique constraint on that, and in
    # the model save method we can prevent clashes if the folder already exists
    name = models.CharField(
        _("Name"),
        unique=True,
        default="{:.0f}".format(timezone.now().timestamp()),
        max_length=42,
    )

    # Time stamps, and logging of who changed user info
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="has_changed_simulations",
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)


class AtlasSimulationInput(models.Model):
    simulation = models.ForeignKey(AtlasSimulation, on_delete=models.CASCADE)
    folder = models.CharField(
        _("Folder"),
        default="/path/to/nfs/queue/SimulationName/",
        max_length=100,
    )

    # Time stamps, and logging of who changed user info
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="has_changed_simulationinputs",
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)


class AtlasSimulationSlurmJob(models.Model):
    """
    models.CASCADE means that if a Simulation model instance is deleted, then
    also the related model instance will be deleted.
    """

    simulation = models.ForeignKey(AtlasSimulation, on_delete=models.CASCADE)
    jobscript = models.CharField(
        _("Folder"),
        default="/path/to/nfs/queue/SimulationName/jobscript.sh",
        max_length=100,
    )

    # Time stamps, and logging of who changed user info
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="has_changed_simulationlurmjobs",
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)


class AtlasSimulationOutput(models.Model):
    simulation = models.ForeignKey(AtlasSimulation, on_delete=models.CASCADE)
    folder = models.CharField(
        _("Folder"), default="/path/to/nfs/processed/SimulationName/", max_length=100
    )

    # Time stamps, and logging of who changed user info
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="has_changed_simulationoutputs",
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)
