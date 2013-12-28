/**
 * Created by cuiwei on 13-12-26.
 */
;(function ($, document, window) {
  var $selectionItem = $('.selection-item');
  var $noteItem = $('.note-item');

  $selectionItem.each(function () {
    var $this = $(this);

    $this.find('.show-note').on('click', function () {
      // selection 展开点评
      $this.find('.common-note').slideToggle('slow');
    });
  });

  // 修改点评
  $noteItem.each(function () {
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

  // 评论
  $noteItem.each(function () {
    var $this = $(this);
    var $noteComment = $this.find('.note-comment');
    var $form = $noteComment.find('form');

    var $replyToUser = $form.find('input[name="reply_to_user_id"]');
    var $replyToComment = $form.find('input[name="reply_to_comment_id"]');
    var $commentText = $form.find('input[name="comment_text"]');

    $this.find('.add-comment').on('click', function () {
      $noteComment.slideToggle('fast');

      $form.find('.cancel-comment').one('click', function () {
        $noteComment.slideUp('fast');

        $replyToUser.val('');
        $replyToComment.val('');
        $commentText.val('');
      });
    });

    $noteComment.find('.reply').on('click', function () {
      var $parent = $(this).parent();
      var $p = $parent.find('.comment-content');
      var $nickname = $parent.find('.nickname');

      $commentText.val('回复 ' + $nickname.text() + ': ');
      $replyToUser.val($p.attr('data-creator'));
      $replyToComment.val($p.attr('data-comment'));
    });

    $form.find('.operate-comment input').on('click', function (e) {
      var commentText = $commentText.val();

      if (commentText.length > 0) {
        var url = $form[0].action;

        $.post(url, $form.serialize(), function (data) {
          $(data).insertBefore($form);
        });
      }

      e.preventDefault();
    });
  });

  // 喜爱 like
  $('.like-entity').on('click', function () {
    var $this = $(this);
    var counter = $this.find('small');
    var entity_id = $this.attr('data-entity');
    var url = '/entity/' + entity_id + '/like/';

    $.post(url, function (data) {
      var count = parseInt(counter.text());
      var result = parseInt(data);

      if (result === 1) {
        counter.text(count + 1);
        $this.addClass('already-like');
      } else if (result === 0) {
        counter.text(count - 1);
        $this.removeClass('already-like');
      } else {
        // 需登录
      }
    });
  });








})(jQuery, document, window);