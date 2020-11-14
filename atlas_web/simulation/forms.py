from django import forms
from django.utils.translation import gettext_lazy as _


class SimulationForm(forms.Form):
    name = forms.CharField(required=True)

    # TODO: clean method can check the form against validators, and e.g.
    # raise ValidationError if there's something wrong
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name != "Miha":
            raise forms.ValidationError(_("Your name has to be Miha"))
