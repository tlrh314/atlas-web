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

    def test_T_eff_below_1500_complains(self, valid_simulation_input_data):
        data_with_T_eff_below_1500 = copy.copy(valid_simulation_input_data)
        data_with_T_eff_below_1500["T_eff"] = "1000"
        form = SimulationForm(data=data_with_T_eff_below_1500)
        assert not form.is_valid()
        assert (
            form.errors["T_eff"][0]
            == "Ensure this value is greater than or equal to 1500."
        )

    def test_T_eff_above_12000_complains(self, valid_simulation_input_data):
        data_with_T_eff_above_12000 = copy.copy(valid_simulation_input_data)
        data_with_T_eff_above_12000["T_eff"] = "13000"
        form = SimulationForm(data=data_with_T_eff_above_12000)
        assert not form.is_valid()
        assert (
            form.errors["T_eff"][0]
            == "Ensure this value is less than or equal to 12000."
        )

    def test_log_G_below_0_complains(self, valid_simulation_input_data):
        data_with_log_G_below_0 = copy.copy(valid_simulation_input_data)
        data_with_log_G_below_0["log_G"] = "-1"
        form = SimulationForm(data=data_with_log_G_below_0)
        assert not form.is_valid()
        assert (
            form.errors["log_G"][0]
            == "Ensure this value is greater than or equal to 0."
        )

    def test_log_G_above_5_complains(self, valid_simulation_input_data):
        data_with_log_G_above_5 = copy.copy(valid_simulation_input_data)
        data_with_log_G_above_5["log_G"] = "6"
        form = SimulationForm(data=data_with_log_G_above_5)
        assert not form.is_valid()
        assert (
            form.errors["log_G"][0] == "Ensure this value is less than or equal to 5."
        )

    def test_vturb_below_0_complains(self, valid_simulation_input_data):
        data_with_vturb_below_0 = copy.copy(valid_simulation_input_data)
        data_with_vturb_below_0["vturb"] = "-1"
        form = SimulationForm(data=data_with_vturb_below_0)
        assert not form.is_valid()
        assert (
            form.errors["vturb"][0]
            == "Ensure this value is greater than or equal to 0."
        )

    def test_vturb_above_5_complains(self, valid_simulation_input_data):
        data_with_vturb_above_5 = copy.copy(valid_simulation_input_data)
        data_with_vturb_above_5["vturb"] = "6"
        form = SimulationForm(data=data_with_vturb_above_5)
        assert not form.is_valid()
        assert (
            form.errors["vturb"][0] == "Ensure this value is less than or equal to 5."
        )

    # def test_data_with_mixing_length_without_convection(self, valid_simulation_input_data):
    #     data_with_mixing_length_without_convection = copy.copy(valid_simulation_input_data)
    #     data_with_mixing_length_without_convection["convection"] = False
    #     data_with_mixing_length_without_convection["mixing_length"] = 2
    #     form = SimulationForm(data=data_with_mixing_length_without_convection)
    #     assert not form.is_valid()
    #     assert (form.errors["mixing_length"][0]
    #         == "Mixing length is only used when convection is enabled.")

    # def mixing_length_when_convection_disabled_complains(self, valid_simulation_input_data):
    #     data_with_mixing_length_without_convection = copy.copy(valid_simulation_input_data)
    #     data_with_mixing_length_without_convection["convection"] = False
    #     data_with_mixing_length_without_convection["mixing_length"] = 2
    #     assert(False)
    #     assert not form_is_valid()
    #     assert (
    #         form.errors["mixing_length"][0]
    #         == "Mixing length is only used when convection is enabled."
    #     )

    # def test_mixing_length_below_0_complains(self, valid_simulation_input_data):
    #     data_with_mixing_length_below_0 = copy.copy(valid_simulation_input_data)
    #     data_with_mixing_length_below_0["mixing_length"] = "-1"
    #    form = SimulationForm(data=data_with_mixing_length_below_0)
    #     assert not form.is_valid()
    #     assert (
    #         form.errors["mixing_length"][0]
    #         == "Ensure this value is greater than or equal to 0."
    #     )

    # def test_mixing_length_above_5_complains(self, valid_simulation_input_data):
    #     data_with_mixing_length_above_6 = copy.copy(valid_simulation_input_data)
    #     data_with_mixing_length_above_6["mixing_length"] = "6"
    #     form = SimulationForm(data=data_with_mixing_length_above_6)
    #     assert not form.is_valid()
    #     assert (
    #         form.errors["mixing_length"][0]
    #         == "Ensure this value is less than or equal to 5."
    #     )

    # def overshoot_when_convection_disabled_complains(self, valid_simulation_input_data):
    #     data_with_overshoot_without_convection = copy.copy(valid_simulation_input_data)
    #     print(data_with_overshoot_without_convection["convection"])
    #     data_with_overshoot_without_convection["convection"] = False
    #     data_with_overshoot_without_convection["overshoot"] = True
    #     assert not form_is_valid()
    #     assert (
    #         form.errors["overshoot"][0]
    #         == "Ensure this value is disabled when convection is disabled."
    #     )
