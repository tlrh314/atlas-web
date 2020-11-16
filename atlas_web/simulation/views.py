from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from atlas_web.simulation.forms import SimulationForm
from atlas_web.simulation.utils import create_atlas_input_file_from_valid_form


def simulation_input_view(request):
    atlas_input_file_content = None

    if request.method == "POST":
        form = SimulationForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            print(_("Your name is {}, we're happy".format(name)))

            atlas_input_file_name = create_atlas_input_file_from_valid_form(
                form.cleaned_data
            )
            with open(atlas_input_file_name, "r") as f:
                atlas_input_file_content = f.read()
    else:
        form = SimulationForm()

    # We can hit this block if request was POST, but the form data was not valid.
    # That way the form errors that sit in the form are served back to the template,
    # where you can show them to the user.
    return render(
        request,
        "simulation/input.html",
        {"form": form, "atlas_input_file_content": atlas_input_file_content},
    )
