/**
 * Created by cuiwei on 13-12-26.
 */
(function ($, document, window) {

  // selection 展开点评
  $('.selection-item .show-note').on('click', function () {
    var $note = $(this).parent().parent();
    $note.find('.common-note').slideToggle('slow');
  });

  $('.note-item').each(function () {
    var $this = $(this);
    var $p = $this.find('p.note-content');
    var $form = $this.find('.update-note-form');
    var $textarea = $form.find('textarea');
    var originNoteText;

    $this.find('.update-note').on('click', function () {
      originNoteText = $textarea.val();
      $p.hide();
      $form.show();

      $form.find('.cancel-update').one('click', function () {
        $textarea.val(originNoteText);
        $form.hide();
        $p.show();
      });
    });

    $this.find('.update-note-form').on('submit', function (e) {
      var noteText = $textarea.val();

      if (noteText !== originNoteText && noteText.length > 0) {
        var url = $form[0].action;

        $.post(url, $form.serialize(), function (data) {
          if (parseInt(data) === 1) {
            $p.text(noteText);
            $form.hide();
            $p.show();
          }
        });
      }

      e.preventDefault();
    });
  });

  // 展开评论
  $('.note-comment .add-comment').on('click', function () {
    var $noteDetail = $(this).parent();
    var $noteComment = $noteDetail.find('.note-comment');
    $noteComment.slideToggle('fast');

    $noteDetail.find('.cancel-comment').one('click', function () {
      $noteComment.slideUp('fast');
    });
  });







})(jQuery, document, window);