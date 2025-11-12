document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(
    'input[type="datetime"], input.vDateField, input.vTimeField, input[type="text"][name$="date"], input[type="text"][name$="datetime"]'
  ).forEach(function (input) {
    flatpickr(input, {
      enableTime: true,
      dateFormat: "Y-m-d H:i",
      allowInput: true,
    });
  });
});
