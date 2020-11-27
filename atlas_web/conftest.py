"""
Note that the conftest makes various things available to the test runner.  For example, most TestCases
need a user, so a new user is conveniently generated using the UserFactory.
"""

import pytest

from atlas_web.simulation.models import AtlasSimulation
from atlas_web.simulation.tests.factories import AtlasSimulationFactory
from atlas_web.users.models import User
from atlas_web.users.tests.factories import AdminFactory, UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def admin() -> User:
    admin = AdminFactory()
    admin.set_password("admin_password")
    admin.save()
    return admin


@pytest.fixture
def simulation() -> AtlasSimulation:
    return AtlasSimulationFactory()


@pytest.fixture
def valid_simulation_input_data() -> dict:
    return {
        "calculation_type": "odf",
        "abundances": "anders",
        "metallicity": "1",
        "T_eff": "5500",
        "log_G": "1",
        "vturb": "2",
        "convection": "on",
        "mixing_length": "2",
        "wavelength_start": "100",
        "wavelength_end": "900",
        "wavelength_step": "900",
        "T_start": "1500",
        "T_end": "1500",
        "T_n": "25",
        "p_start": "-3",
        "p_end": "8",
        "p_n": "25",
    }
