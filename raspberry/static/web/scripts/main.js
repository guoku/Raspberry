/**
 * Created by cuiwei on 13-12-26.
 */
(function ($, document, window) {

  // selection 展开点评
  $('.selection-item a.show-note').on('click', function () {
    var $note = $(this).parent().parent();
    $note.find('.more-note').slideToggle('slow');
  });

  // 修改点评
  $('.note-item a.update-note').on('click', function () {
    var $noteDetail = $(this).parent();
    var $p = $noteDetail.find('p').hide();
    var $form = $noteDetail.find('form').slideDown('fast');
    var $textarea = $form.find('textarea');
    var originNote = $textarea.val();

    $noteDetail.find('.cancel-update').one('click', function () {
      $textarea.val(originNote);
      $p.show();
      $form.slideUp('fast');
    });

    $form.on('submit', function (e) {
      var noteText = $textarea.val();

      if (noteText != originNote && noteText.length > 0) {
        var url = $form[0].action;

        $.post(url, $form.serialize(), function (data) {
          if (parseInt(data) === 1) {
            $p.text(noteText);
            $p.show();
            $form.slideUp('fast');
          }
        });
      }

      e.preventDefault();
    });
  });

  // 展开评论
  $('.note-item a.add-comment').on('click', function () {
    var $noteDetail = $(this).parent();
    var $noteComment = $noteDetail.find('.note-comment');
    $noteComment.slideToggle('fast');

    $noteDetail.find('.cancel-comment').one('click', function () {
      $noteComment.slideUp('fast');
    });
  });







})(jQuery, document, window);