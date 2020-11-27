import glob

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from atlas_web.simulation.forms import SimulationForm
from atlas_web.simulation.models import AtlasSimulation
from atlas_web.simulation.utils import create_atlas_input_files_from_valid_form


def simulation_input_view(request):
    atlas9_punched_input = None
    atlas9_in_odf = None
    atlas9_in_model = None
    atlas9_in_flux = None
    atlas9_control = None

    if request.method == "POST":
        form = SimulationForm(data=request.POST)
        if form.is_valid():
            # Create a new AtlasSimulation instance that will mkdir the simulation folders
            simulation = AtlasSimulation()
            simulation.save()

            create_atlas_input_files_from_valid_form(
                form.cleaned_data, simulation.input.folder
            )

            path_to_atlas9_punched_input = None
            path_to_atlas9_in_odf = None
            path_to_atlas9_in_model = None
            path_to_atlas9_in_flux = None
            path_to_atlas9_control = None

            for atlas_input_file in glob.glob("{}*".format(simulation.input.folder)):
                if "punched.input" in atlas_input_file:
                    path_to_atlas9_punched_input = atlas_input_file
                if "inODF" in atlas_input_file:
                    path_to_atlas9_in_odf = atlas_input_file
                    success_msg = "ODF"
                if "inMODEL" in atlas_input_file:
                    path_to_atlas9_in_model = atlas_input_file
                    success_msg = "MODEL"
                if "inFLUX" in atlas_input_file:
                    path_to_atlas9_in_flux = atlas_input_file
                    success_msg = "FLUX"
                if "control" in atlas_input_file:
                    path_to_atlas9_control = atlas_input_file

            if path_to_atlas9_punched_input:
                with open(path_to_atlas9_punched_input, "r") as f:
                    atlas9_punched_input = f.read()
            if path_to_atlas9_in_odf:
                with open(path_to_atlas9_in_odf, "r") as f:
                    atlas9_in_odf = f.read()
            if path_to_atlas9_in_model:
                with open(path_to_atlas9_in_model, "r") as f:
                    atlas9_in_model = f.read()
            if path_to_atlas9_in_flux:
                with open(path_to_atlas9_in_flux, "r") as f:
                    atlas9_in_flux = f.read()
            if path_to_atlas9_control:
                with open(path_to_atlas9_control, "r") as f:
                    atlas9_control = f.read()

            messages.add_message(
                request,
                messages.SUCCESS,
                _(
                    "Your input is valid! The atlas code files are listed below. Type: {}".format(
                        success_msg
                    )
                ),
            )

    else:
        form = SimulationForm()

    # We can hit this block if request was POST, but the form data was not valid.
    # That way the form errors that sit in the form are served back to the template,
    # where you can show them to the user.
    return render(
        request,
        "simulation/input.html",
        {
            "form": form,
            "atlas9_punched_input": atlas9_punched_input,
            "atlas9_in_odf": atlas9_in_odf,
            "atlas9_in_model": atlas9_in_model,
            "atlas9_in_flux": atlas9_in_flux,
            "atlas9_control": atlas9_control,
        },
    )
