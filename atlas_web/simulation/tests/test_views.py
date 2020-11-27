import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from atlas_web.simulation.models import AtlasSimulation
from atlas_web.simulation.views import (
    simulation_detail_view,
    simulation_input_view,
    simulation_list_view,
)

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestSimulationView:
    def test_simulation_input_view_anonymous(self, rf: RequestFactory):
        url = reverse("simulation:input")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = simulation_input_view(request)
        assert response.status_code == 302
        assert response.url == "/users/login/?next={}".format(url)

    def test_simulation_input_view_post_valid_data(
        self, valid_simulation_input_data, client: Client, admin: User
    ):
        login_status = client.login(
            email=admin.email, password="admin_password"
        )  # pytest.fixture in atlas_web/conftest.py
        assert login_status

        response = client.post(
            reverse("simulation:input"), data=valid_simulation_input_data
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/input.html")

    def test_simulation_list_view_anonymous_302_to_login(
        self, rf: RequestFactory, simulation: AtlasSimulation
    ):
        url = reverse("simulation:list")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = simulation_list_view(request)
        assert response.status_code == 302
        assert response.url == "/users/login/?next={}".format(url)

    def test_simulation_list_view_when_user_started_1_simulation(
        self, client: Client, admin: User, simulation: AtlasSimulation
    ):
        """ Let's log a user in, add that user to 1 simulation as requested_by """

        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 0
        simulation.requested_by = admin
        simulation.save()
        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 1

        login_status = client.login(email=admin.email, password="admin_password")
        assert login_status

        simulation_detail = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        url = reverse("simulation:list")
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/list.html")

        # Check the blocks that show simulations started / additional simulations are correct
        assertContains(
            response, '<div class="card-header">Simulation started by me</div>'
        )
        assertNotContains(response, "You did not request any simulations yet")
        assertNotContains(
            response, '<div class="card-header">Simulation I also have access to</div>'
        )

        # Check that there's only 1 simulation available for this user
        # Note that this one will sit in the "Simulation started by me" card.
        assertContains(response, "<tr><th>", count=1)

        # And check that this simulation is the simulation we put
        assertContains(
            response,
            '<tr><th><a href="{}">{}</a></th></tr>'.format(
                simulation_detail, simulation.name
            ),
        )

    def test_simulation_list_view_when_user_has_access_to_1_additional_simulation(
        self, client: Client, admin: User, simulation: AtlasSimulation
    ):
        """ Let's log a user in, add that user to 1 simulation as access_list """

        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 0
        simulation.access_list.add(admin)
        assert admin.has_access_to_simulations.count() == 1
        assert admin.simulations_started.count() == 0

        login_status = client.login(email=admin.email, password="admin_password")
        assert login_status

        simulation_detail = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        url = reverse("simulation:list")
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/list.html")

        # Check the blocks that show simulations started / additional simulations are correct
        assertContains(
            response, '<div class="card-header">Simulation started by me</div>'
        )
        assertContains(response, "You did not request any simulations yet")
        assertContains(
            response, '<div class="card-header">Simulation I also have access to</div>'
        )

        # Check that there's only 1 simulation available for this user.
        # Note that this one will sit in the "Simulation I also have access to" card.
        assertContains(response, "<tr><th>", count=1)

        # And check that this simulation is the simulation we put
        assertContains(
            response,
            '<tr><th><a href="{}">{}</a></th></tr>'.format(
                simulation_detail, simulation.name
            ),
        )

    def test_simulation_detail_view_anonymous_302_to_login(
        self, rf: RequestFactory, admin: User, simulation: AtlasSimulation
    ):

        url = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        request = rf.get(url)
        request.user = AnonymousUser()
        response = simulation_detail_view(request, pk=simulation.pk)
        assert response.status_code == 302
        assert response.url == "/users/login/?next={}".format(url)

    def test_simulation_detail_view_is_authenticated_403_for_simulations_no_access(
        self, client: Client, admin: User, simulation: AtlasSimulation
    ):
        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 0

        login_status = client.login(email=admin.email, password="admin_password")
        assert login_status

        url = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        response = client.get(url)
        assert response.status_code == 403

    def test_simulation_detail_view_when_user_started_1_simulation(
        self, client: Client, admin: User, simulation: AtlasSimulation
    ):
        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 0
        simulation.requested_by = admin
        simulation.save()
        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 1

        login_status = client.login(email=admin.email, password="admin_password")
        assert login_status

        url = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/detail.html")

    def test_simulation_detail_view_when_user_has_access_to_1_additional_simulation(
        self, client: Client, admin: User, simulation: AtlasSimulation
    ):
        assert admin.has_access_to_simulations.count() == 0
        assert admin.simulations_started.count() == 0
        simulation.access_list.add(admin)
        assert admin.has_access_to_simulations.count() == 1
        assert admin.simulations_started.count() == 0

        login_status = client.login(email=admin.email, password="admin_password")
        assert login_status

        url = reverse("simulation:detail", kwargs={"pk": simulation.pk})
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "simulation/detail.html")
