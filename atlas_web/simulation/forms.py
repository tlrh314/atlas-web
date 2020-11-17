from django import forms
from django.utils.translation import gettext_lazy as _


class SimulationForm(forms.Form):
    ABUNDANCE_CHOICES = [
        ("anders", "Anders"),
        ("asplund", "Asplund"),
        ("grevess", "Grevess"),
    ]
    TEMPERATURE_CHOICES = [("standard", "Standard"), ("non-standard", "Non-standard")]
    PRESSURE_CHOICES = [("standard", "Standard"), ("non-standard", "Non-standard")]

    name = forms.CharField(required=True)
    abundances = forms.ChoiceField(
        label=_("Abundances"), required=True, choices=ABUNDANCE_CHOICES
    )

    metallicity = forms.FloatField(
        required=True,
        min_value=-4,
        max_value=2,
        widget=forms.NumberInput(attrs={"id": "form_metallicity", "step": "0.1"}),
        label=_("Metallicity in units of solar metallicity"),
    )
    T_eff = forms.FloatField(
        required=True,
        min_value=1500,
        max_value=12000,
        widget=forms.NumberInput(attrs={"id": "form_T_eff", "step": "100"}),
        label=_("Effective temperature of the model"),
    )
    log_G = forms.FloatField(
        required=True,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={"id": "form_log_G", "step": ".1"}),
        label=_("log G of the model"),
    )
    vturb = forms.FloatField(
        required=True,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={"id": "form_vturb", "step": ".1"}),
        label=_("Turbulent Velocity in km/s"),
    )

    convection = forms.BooleanField(label=_("Enable Convection?"), required=True)
    mixing_length = forms.FloatField(
        required=False,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={"id": "form_mixing_length", "step": "1"}),
        label=_("Mixing length in km, only used when convection is enabled."),
    )
    overshoot = forms.BooleanField(label=_("Include overshoot?"))
    wavelength_grid = forms.ChoiceField(label=_("Wavelength grid"), required=True)
    T_grid = forms.ChoiceField(
        label=_("Temperature grid"), required=True, choices=TEMPERATURE_CHOICES
    )
    p_grid = forms.ChoiceField(
        label=_("Pressure grid"), required=True, choices=PRESSURE_CHOICES
    )

    # TODO: clean method can check the form against validators, and e.g.
    # raise ValidationError if there's something wrong
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        convection = cleaned_data.get("convection")
        mixing_length = cleaned_data.get("mixing_length")
        overshoot = cleaned_data.get("overshoot")

        if name != "Miha":
            raise forms.ValidationError(_("Your name has to be Miha"))
        if not convection:
            if mixing_length is not None:
                raise forms.ValidationError(
                    _("Mixing length is only used when convection is enabled.")
                )
            if overshoot:
                raise forms.ValidationError(
                    _("Overshoot is only used when convection is enabled.")
                )
        if convection:
            if mixing_length is None:
                raise forms.ValidationError(
                    _("Missing mixing length when convection is enabled.")
                )
