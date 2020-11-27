from django.urls import resolve, reverse

import atlas_web.simulation.views as simulation_views


def test_simulation_input():
    url = reverse("simulation:input")
    assert url == "/simulation/input/"

    resolver = resolve(url)
    assert resolver.func == simulation_views.simulation_input_view
    assert resolver.namespace == "simulation"
    assert resolver.view_name == "simulation:input"


def test_simulation_list():
    url = reverse("simulation:list")
    assert url == "/simulation/list/"

    resolver = resolve(url)
    assert resolver.func == simulation_views.simulation_list_view
    assert resolver.namespace == "simulation"
    assert resolver.view_name == "simulation:list"


def test_simulation_detail():
    url = reverse("simulation:detail", kwargs={"pk": 1337})
    assert url == "/simulation/detail/1337/"

    resolver = resolve(url)
    assert resolver.func == simulation_views.simulation_detail_view
    assert resolver.namespace == "simulation"
    assert resolver.view_name == "simulation:detail"
