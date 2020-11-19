from django.urls import resolve, reverse

import atlas_web.simulation.views as simulation_views


def test_simulation_input():
    url = reverse("simulation:input")
    assert url == "/simulation/input/"

    resolver = resolve(url)
    assert resolver.func == simulation_views.simulation_input_view
    assert resolver.namespace == "simulation"
    assert resolver.view_name == "simulation:input"
