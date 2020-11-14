from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from atlas_web.simulation.forms import SimulationForm


def simulation_input_view(request):
    # TODO: implement the logic for the view here
    if request.method == "POST":
        form = SimulationForm(data=request.POST)
        print(form)  # print goes to Django log, see /w e.g. `docker logs -f django`

        if form.is_valid():
            name = form.cleaned_data["name"]
            print("Your name is Miha, we're happy")
            print("Your name is Miha, we're happy")
            print("Your name is Miha, we're happy")
            print("Your name is Miha, we're happy")
            print("Your name is Miha, we're happy")
    else:
        form = SimulationForm()

    # We can hit this block if request was POST, but the form data was not valid.
    # That way the form errors that sit in the form are served back to the template,
    # where you can show them to the user.
    return render(request, "simulation/input.html", {"form": form})
