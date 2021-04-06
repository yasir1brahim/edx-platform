
(function ($) {
  $(document).ready(function () {
    $('#submitRating').on("click", function() {
      let rating = $('#rateit-range-3').attr('aria-valuenow');
      let review = $('#feedbackTextarea').val();
      let url = $('#submitRating').data('url');
      $.ajax({
        type: "POST",
        url: url,
        data: {
          "rating": rating,
          "review": review,
        },
        success: function (){
          location.reload();
        }
      });
    })
  });
}(jQuery));
