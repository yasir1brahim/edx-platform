$(document).ready(function() {
  'use strict';

  $('.js-mark-read-status').on('click', function(ev) {
    ev.preventDefault();
    var $ev = $(ev.currentTarget);
    var url = $ev.data('url');
    var isRead = $ev.data('is-read');
    $.ajax({
        url: url,
        type: 'PUT',
        data: {is_read: !isRead},
        success: function (result) {
          if (!isRead) {
            $ev.parents('.js-item-notification').removeClass('new-notification');
            $ev.children('.js-mark-as-read').addClass('hidden');
            $ev.children('.js-mark-as-unread').removeClass('hidden');
          }
          else {
            $ev.parents('.js-item-notification').addClass('new-notification');
            $ev.children('.js-mark-as-read').removeClass('hidden');
            $ev.children('.js-mark-as-unread').addClass('hidden');
          }
          $ev.data('is-read', !isRead);
        },
    });
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
