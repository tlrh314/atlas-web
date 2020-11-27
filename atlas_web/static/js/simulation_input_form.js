$(document).ready(function () {
  showFormForOdf();
});

$(document).on("change", "select[id=\"id_calculation_type\"]", function () {
  if (this.value === "odf") {
    showFormForOdf();
  } else if (this.value === "model") {
    showFormForModel();
  } else if (this.value === "flux") {
    showFormForFlux();
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
  $("input[id=\"p_step\"]").prop("disabled", false);
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
  $("input[id=\"T_step\"]").val(57);

  $("input[id=\"p_step\"]").prop("disabled", true);
  $("input[id=\"p_step\"]").val(25);
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
  $("input[id=\"T_step\"]").prop("disabled", true);
  $("input[id=\"p_step\"]").prop("disabled", true);
}
