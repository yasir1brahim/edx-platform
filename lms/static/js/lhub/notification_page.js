$(document).ready(function() {
  'use strict';

  $('.js-mark-as-read').on('click', function(ev) {
    ev.preventDefault();
    var $ev = $(ev.currentTarget);
    var url = $ev.data('url');
    $.ajax({
        url: url,
        type: 'PUT',
        data: {is_read: true}
    });
    $ev.parents('.new-notification').removeClass('new-notification');
    $ev.remove();
  });

  $('.js-delete-notification').on('click', function(ev) {
    ev.preventDefault();
    var $ev = $(ev.currentTarget);
    var url = $ev.data('url');
    $.ajax({
        url: url,
        type: 'DELETE',
    });
    $ev.parents('.js-item-notification').remove();
  });
});
