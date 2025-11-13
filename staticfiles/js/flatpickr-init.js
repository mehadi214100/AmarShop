document.addEventListener("DOMContentLoaded", function () {
  
  document.querySelectorAll('input.vDateField').forEach(function (input) {
    flatpickr(input, {
      dateFormat: "Y-m-d",
      allowInput: true,
    });
  });

  document.querySelectorAll('input.vTimeField').forEach(function (input) {
    flatpickr(input, {
      enableTime: true,
      noCalendar: true,
      dateFormat: "H:i",
      allowInput: true,
    });
  });
});
