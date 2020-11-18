from django import forms
from django.utils.translation import gettext_lazy as _


class SimulationForm(forms.Form):
    ABUNDANCE_CHOICES = [
        ("anders", "Anders"),
        ("asplund", "Asplund"),
        ("grevess", "Grevess"),
    ]

    CALCULATION_TYPE_CHOICES = [("odf", "ODF"), ("model", "Model"), ("flux", "Flux")]

    calculation_type = forms.ChoiceField(
        label=_("Type of calculation to perform"),
        required=True,
        choices=CALCULATION_TYPE_CHOICES,
    )

    abundances = forms.ChoiceField(
        label=_("Abundances"), required=True, choices=ABUNDANCE_CHOICES
    )

    metallicity = forms.FloatField(
        required=True,
        min_value=-4,
        max_value=2,
        initial=1,
        widget=forms.NumberInput(
            attrs={"id": "form_metallicity", "default": "1", "step": "0.1"}
        ),
        label=_("Metallicity in units of solar metallicity"),
    )
    T_eff = forms.FloatField(
        required=True,
        min_value=1500,
        max_value=12000,
        initial=5500,
        widget=forms.NumberInput(attrs={"id": "form_T_eff", "step": "100"}),
        label=_("Effective temperature of the model"),
    )
    log_G = forms.FloatField(
        required=True,
        min_value=0,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"id": "form_log_G", "step": ".1"}),
        label=_("log G of the model"),
    )
    vturb = forms.FloatField(
        required=True,
        min_value=0,
        max_value=5,
        initial=2,
        widget=forms.NumberInput(attrs={"id": "form_vturb", "step": ".1"}),
        label=_("Turbulent Velocity in km/s"),
    )

    convection = forms.BooleanField(label=_("Enable Convection?"), initial=True)
    mixing_length = forms.FloatField(
        required=False,
        min_value=0,
        max_value=5,
        initial=2,
        widget=forms.NumberInput(attrs={"id": "form_mixing_length", "step": "1"}),
        label=_("Mixing length in km, only used when convection is enabled."),
    )
    overshoot = forms.BooleanField(label=_("Include overshoot?"), required=False)

    wavelength_start = forms.FloatField(
        required=True,
        min_value=100,
        max_value=2000,
        initial=100,
        widget=forms.NumberInput(attrs={"id": "wavelength_start", "step": "1"}),
        label=_("Starting Wavelength in nm"),
    )

    wavelength_end = forms.FloatField(
        required=True,
        min_value=100,
        max_value=2000,
        initial=900,
        widget=forms.NumberInput(attrs={"id": "wavelength_end", "step": "1"}),
        label=_("End Wavelength in nm"),
    )
    wavelength_step = forms.FloatField(
        required=True,
        min_value=100,
        max_value=2000,
        initial=900,
        widget=forms.NumberInput(attrs={"id": "wavelength_step", "step": "1"}),
        label=_("Wavelength step in nm"),
    )

    T_start = forms.FloatField(
        required=True,
        min_value=1500,
        max_value=12000,
        initial=1500,
        widget=forms.NumberInput(attrs={"id": "wavelength_start", "step": "1"}),
        label=_("Starting Temperature K"),
    )

    T_end = forms.FloatField(
        required=True,
        min_value=1500,
        max_value=12000,
        initial=1500,
        widget=forms.NumberInput(attrs={"id": "wavelength_end", "step": "1"}),
        label=_("End Temperature in K"),
    )
    T_n = forms.FloatField(
        required=True,
        min_value=3,
        max_value=100,
        initial=25,
        widget=forms.NumberInput(attrs={"id": "wavelength_step", "step": "1"}),
        label=_("Number of T bins"),
    )

    p_start = forms.FloatField(
        required=True,
        min_value=-5,
        max_value=9,
        initial=-3,
        widget=forms.NumberInput(attrs={"id": "p_start", "step": "1"}),
        label=_("Starting pressure"),
    )

    p_end = forms.FloatField(
        required=True,
        min_value=-5,
        max_value=9,
        initial=8,
        widget=forms.NumberInput(attrs={"id": "p_end", "step": "1"}),
        label=_("End Pressure"),
    )
    p_n = forms.FloatField(
        required=True,
        min_value=3,
        max_value=100,
        initial=25,
        widget=forms.NumberInput(attrs={"id": "p_step", "step": "1"}),
        label=_("Number of Pressure bins"),
    )

    # T_grid = forms.ChoiceField(label=_("Temperature grid"), choices=TEMPERATURE_CHOICES)
    # p_grid = forms.ChoiceField(label=_("Pressure grid"), choices=PRESSURE_CHOICES)

    # TODO: clean method can check the form against validators, and e.g.
    # raise ValidationError if there's something wrong
    def clean(self):
        cleaned_data = super().clean()
        convection = cleaned_data.get("convection")
        mixing_length = cleaned_data.get("mixing_length")
        overshoot = cleaned_data.get("overshoot")

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
