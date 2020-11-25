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
        blank=True,
        max_length=42,
        help_text=_("Unique identifier for this simulation. This is auto-set on save."),
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="simulations_started",
    )

    access_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="has_access_to_simulations",
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

    def save(self, *args, **kwargs):
        self.name = "{:.0f}".format(timezone.now().timestamp())
        input = AtlasSimulationInput(
            simulation=self, folder="/path/to/nfs/queue/{}/".format(self.name)
        )
        slurmjob = AtlasSimulationSlurmJob(
            simulation=self,
            jobscript="/path/to/nfs/queue/{}/jobscript.sh".format(self.name),
        )
        output = AtlasSimulationOutput(
            simulation=self, folder="/path/to/nfs/processed/{}/".format(self.name)
        )

        super().save()
        input.save()
        slurmjob.save()
        output.save()

    def __str__(self):
        return "AtlasSimulation {}".format(self.name)


class AtlasSimulationInput(models.Model):
    simulation = models.OneToOneField(
        AtlasSimulation, on_delete=models.CASCADE, related_name="input"
    )
    folder = models.CharField(
        _("Folder"),
        max_length=100,
        help_text=_("Path to the simulation input folder. This is auto-set on save."),
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

    def __str__(self):
        return "{}".format(self.simulation.name)


class AtlasSimulationSlurmJob(models.Model):
    """
    models.CASCADE means that if a Simulation model instance is deleted, then
    also the related model instance will be deleted.
    """

    simulation = models.OneToOneField(
        AtlasSimulation, on_delete=models.CASCADE, related_name="slurmjob"
    )
    jobscript = models.CharField(
        _("Folder"),
        max_length=100,
        help_text=_("Path to the simulation jobscript. This is auto-set on save."),
    )
    SLURM_STATUS = (
        (0, "Created"),
        (1, "Queued"),
        (2, "Starting"),
        (3, "Running"),
        (4, "Paused"),
        (5, "Failed"),
        (6, "Interrupted"),
        (7, "Cancelled"),
        (8, "Retried"),
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), default=0, choices=SLURM_STATUS
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

    def __str__(self):
        return "{}".format(self.simulation.name)


class AtlasSimulationOutput(models.Model):
    simulation = models.OneToOneField(
        AtlasSimulation, on_delete=models.CASCADE, related_name="output"
    )
    folder = models.CharField(
        _("Folder"),
        max_length=100,
        help_text=_("Path to the simulation output folder. This is auto-set on save."),
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

    def __str__(self):
        return "{}".format(self.simulation.name)
