$(document).on("change", "select[id=\"id_calculation_type\"]", function () {
  if (this.value === "odf") {
    showFormForOdf();
  } else if (this.value === "model") {
    showFormForModel();
  } else if (this.value === "flux") {
    showFormForFlux();
  }
});

$(document).on("change", "select[id=\"id_wavelength\"]", function () {
  if (this.value === "standard") {
    hideWavelength();
  } else if (this.value === "nonstandard") {
    showWavelength();
  }
});

$(document).on("change", "select[id=\"id_temperature\"]", function () {
  if (this.value === "standard") {
    hideTemperature();
  } else if (this.value === "nonstandard") {
    showTemperature();
  }
});

$(document).on("change", "select[id=\"id_pressure\"]", function () {
  if (this.value === "standard") {
    hidePressure();
  } else if (this.value === "nonstandard") {
    showPressure();
  }
});

$(document).on("change", "input[id=\"id_convection\"]", function () {
  if ($(this).is(":checked")) {
    $("input[id=\"form_mixing_length\"]").show();
    $("label[for=\"form_mixing_length\"]").show();
    $("input[id=\"id_overshoot\"]").show();
    $("label[for=\"id_overshoot\"]").show();
  } else {
    $("input[id=\"form_mixing_length\"]").hide();
    $("label[for=\"form_mixing_length\"]").hide();
    $("input[id=\"id_overshoot\"]").hide();
    $("label[for=\"id_overshoot\"]").hide();
  }
});

function showFormForOdf () {
  console.log("Showing the fields for odf");

  $("input[id=\"form_T_eff\"]").hide();
  $("label[for=\"form_T_eff\"]").hide();

  $("input[id=\"form_log_G\"]").hide();
  $("label[for=\"form_log_G\"]").hide();

  $("input[id=\"id_convection\"]").hide();
  $("label[for=\"id_convection\"]").hide();

  $("input[id=\"form_mixing_length\"]").hide();
  $("label[for=\"form_mixing_length\"]").hide();
  $("input[id=\"id_overshoot\"]").hide();
  $("label[for=\"id_overshoot\"]").hide();

  $("input[id=\"T_step\"]").prop("disabled", false);
  $("input[id=\"T_step\"]").attr("value", "25");
  $("input[id=\"p_step\"]").prop("disabled", false);
  $("input[id=\"p_step\"]").attr("value", "25");
}

function showFormForModel () {
  console.log("Showing the fields for model");

  $("input[id=\"form_T_eff\"]").show();
  $("label[for=\"form_T_eff\"]").show();

  $("input[id=\"form_log_G\"]").show();
  $("label[for=\"form_log_G\"]").show();

  $("input[id=\"id_convection\"]").show();
  $("label[for=\"id_convection\"]").show();

  // Hide by default b/c "Enable Convection" is False by default
  $("input[id=\"form_mixing_length\"]").hide();
  $("label[for=\"form_mixing_length\"]").hide();
  $("input[id=\"id_overshoot\"]").hide();
  $("label[for=\"id_overshoot\"]").hide();

  // Non configurable: T-p: standard 57 in T and 25 in p
  $("input[id=\"T_step\"]").prop("disabled", true);
  $("input[id=\"T_step\"]").attr("value", "57");

  $("input[id=\"p_step\"]").prop("disabled", true);
  $("input[id=\"p_step\"]").attr("value", "25");
}

function showFormForFlux () {
  console.log("Showing the fields for flux");

  $("input[id=\"form_T_eff\"]").show();
  $("label[for=\"form_T_eff\"]").show();

  $("input[id=\"form_log_G\"]").show();
  $("label[for=\"form_log_G\"]").show();

  $("input[id=\"id_convection\"]").show();
  $("label[for=\"id_convection\"]").show();

  // Hide by default b/c "Enable Convection" is False by default
  $("input[id=\"form_mixing_length\"]").hide();
  $("label[for=\"form_mixing_length\"]").hide();
  $("input[id=\"id_overshoot\"]").hide();
  $("label[for=\"id_overshoot\"]").hide();

  // Non configurable: T-p (depends on wavelength grid, whether it is high or low resolution)
  hideTemperature();
  hidePressure();
}

function showWavelength () {
  $("input[id=\"wavelength_start\"]").show();
  $("label[for=\"wavelength_start\"]").show();

  $("input[id=\"wavelength_end\"]").show();
  $("label[for=\"wavelength_end\"]").show();

  $("input[id=\"wavelength_step\"]").show();
  $("label[for=\"wavelength_step\"]").show();
}
function hideWavelength () {
  $("input[id=\"wavelength_start\"]").hide();
  $("label[for=\"wavelength_start\"]").hide();

  $("input[id=\"wavelength_end\"]").hide();
  $("label[for=\"wavelength_end\"]").hide();

  $("input[id=\"wavelength_step\"]").hide();
  $("label[for=\"wavelength_step\"]").hide();
}

function showTemperature () {
  $("input[id=\"T_start\"]").show();
  $("label[for=\"T_start\"]").show();

  $("input[id=\"T_end\"]").show();
  $("label[for=\"T_end\"]").show();

  $("input[id=\"T_step\"]").show();
  $("label[for=\"T_step\"]").show();
}
function hideTemperature () {
  $("input[id=\"T_start\"]").hide();
  $("label[for=\"T_start\"]").hide();

  $("input[id=\"T_end\"]").hide();
  $("label[for=\"T_end\"]").hide();

  $("input[id=\"T_step\"]").hide();
  $("label[for=\"T_step\"]").hide();
}

function showPressure () {
  $("input[id=\"p_start\"]").show();
  $("label[for=\"p_start\"]").show();

  $("input[id=\"p_end\"]").show();
  $("label[for=\"p_end\"]").show();

  $("input[id=\"p_step\"]").show();
  $("label[for=\"p_step\"]").show();
}
function hidePressure () {
  $("input[id=\"p_start\"]").hide();
  $("label[for=\"p_start\"]").hide();

  $("input[id=\"p_end\"]").hide();
  $("label[for=\"p_end\"]").hide();

  $("input[id=\"p_step\"]").hide();
  $("label[for=\"p_step\"]").hide();
}
