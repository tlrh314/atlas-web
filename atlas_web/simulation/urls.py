from django.urls import path

from atlas_web.simulation.views import simulation_input_view

app_name = "simulation"
urlpatterns = [
    path("input/", simulation_input_view, name="input"),
]
