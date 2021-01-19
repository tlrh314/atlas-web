import os
import shutil

import pytest
from django.conf import settings

from atlas_web.simulation.models import (
    AtlasSimulation,
    AtlasSimulationInput,
    AtlasSimulationOutput,
    AtlasSimulationSlurmJob,
)

pytestmark = pytest.mark.django_db


class TestAtlasSimulation:
    def test_factory(self, simulation: AtlasSimulation):
        assert simulation.name[0:6] == "Test: "

    def test_save_creates_input_jobscript_output(self, simulation: AtlasSimulation):
        # We put "Test: " in the name of the simulation when created by the factory
        # to distinguish between "real" and "mock" instances, but the folder is created
        # w/o "Test: " in the name (on save, before the factory's post_generation runs).
        name = simulation.name.replace("Test: ", "")

        assert isinstance(simulation.input, AtlasSimulationInput)
        assert simulation.input.folder == "{}/queue/{}/".format(settings.NFS_DIR, name)
        assert os.path.exists(simulation.input.folder)
        assert os.path.isdir(simulation.input.folder)

        assert isinstance(simulation.slurmjob, AtlasSimulationSlurmJob)
        assert simulation.slurmjob.jobscript == "{}/queue/{}/jobscript.sh".format(
            settings.NFS_DIR, name
        )

        assert isinstance(simulation.output, AtlasSimulationOutput)
        assert simulation.output.folder == "{}/processed/{}/".format(
            settings.NFS_DIR, name
        )

        # Clean up the folder created by the test intance
        # TODO: this does not cleanup folders when the test fails, so an approach
        # using a pytest fixture may have to be implemented (or setUp + tearDown
        # to create the simulation instance + delete the input.folder)
        shutil.rmtree(simulation.input.folder)  # remove recursively
