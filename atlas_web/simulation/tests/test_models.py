import os

import pytest

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
        assert simulation.input.folder == "/app/nfs/queue/{}/".format(name)
        assert os.path.exists(simulation.input.folder)
        assert os.path.isdir(simulation.input.folder)

        assert isinstance(simulation.slurmjob, AtlasSimulationSlurmJob)
        assert simulation.slurmjob.jobscript == "/app/nfs/queue/{}/jobscript.sh".format(
            name
        )

        assert isinstance(simulation.output, AtlasSimulationOutput)
        assert simulation.output.folder == "/app/nfs/processed/{}/".format(name)

        # Clean up the folder created by the test intance
        # TODO: this does not cleanup folders when the test fails, so an approach
        # using a pytest fixture may have to be implemented (or setUp + tearDown
        # to create the simulation instance + delete the input.folder)
        os.rmdir(simulation.input.folder)  # assuming the folder is empty
