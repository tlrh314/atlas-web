import copy

import pytest

from atlas_web.simulation.forms import SimulationForm

pytestmark = pytest.mark.django_db


class TestSimulationForm:
    def test_metallicity_below_minus4_complains(self, valid_simulation_input_data):
        """ Take valid_simulation_input_data fixture from atlas_web/conftest.py """
        # Just check one of the values set in the fixtures, to check te fixtures work
        assert valid_simulation_input_data["metallicity"] == "1"

        data_with_metallicity_below_minus_4 = copy.copy(valid_simulation_input_data)
        data_with_metallicity_below_minus_4["metallicity"] = "-5"
        form = SimulationForm(data=data_with_metallicity_below_minus_4)
        assert not form.is_valid()
        assert (
            form.errors["metallicity"][0]
            == "Ensure this value is greater than or equal to -4."
        )

    def test_metallicity_above_plus2_complains(self, valid_simulation_input_data):
        data_with_metallicity_above_plus_2 = copy.copy(valid_simulation_input_data)
        data_with_metallicity_above_plus_2["metallicity"] = "3"
        form = SimulationForm(data=data_with_metallicity_above_plus_2)
        assert not form.is_valid()
        assert (
            form.errors["metallicity"][0]
            == "Ensure this value is less than or equal to 2."
        )
