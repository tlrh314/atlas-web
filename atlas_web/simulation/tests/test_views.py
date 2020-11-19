import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from atlas_web.simulation.views import simulation_input_view

pytestmark = pytest.mark.django_db


class TestSimulationView:
    def test_simulation_input_view_anonymous(self, rf: RequestFactory):
        """
        TODO: at some point this should redirect to login, if form only available
        to logged in users. But that depends on the product requirements an the
        acceptance criteria set by Veronika.
        """
        request = rf.get(reverse("simulation:input"))
        request.user = AnonymousUser()
        response = simulation_input_view(request)
        assert response.status_code == 200

    def test_simulation_input_view_post_valid_data(
        self, valid_simulation_input_data, client: Client, rf: RequestFactory
    ):
        response = client.post(
            reverse("simulation:input"), data=valid_simulation_input_data
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/input.html")
