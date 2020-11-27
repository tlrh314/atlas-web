from django.urls import path

from atlas_web.simulation.views import (
    simulation_detail_view,
    simulation_input_view,
    simulation_list_view,
)

app_name = "simulation"
urlpatterns = [
    path("input/", simulation_input_view, name="input"),
    path("list/", simulation_list_view, name="list"),
    path("detail/<pk>", simulation_detail_view, name="detail"),
]
