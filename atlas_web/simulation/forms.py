from django import forms
from django.utils.translation import gettext_lazy as _


class SimulationForm(forms.Form):
    ABUNDANCE_CHOICES = [
        ("anders", "Anders"),
        ("asplund", "Asplund"),
        ("grevess", "Grevess"),
    ]

    name = forms.CharField(required=True)
    abundances = forms.ChoiceField(
        label=_("Abundances"), required=True, choices=ABUNDANCE_CHOICES
    )

    # TODO: clean method can check the form against validators, and e.g.
    # raise ValidationError if there's something wrong
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name != "Miha":
            raise forms.ValidationError(_("Your name has to be Miha"))
