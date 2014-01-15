/**
 * Created by cuiwei on 13-12-26.
 */
;(function ($, document, window) {
    // 动态加载selection
    (function () {
        var $selection = $('#selection');
        if ($selection[0]) {
            var counter = 1;
            var top = 2800 * counter;

            $(window).scroll(function () {
                var $this = $(this);

                if ($this.scrollTop() > top) {
                    counter++;
                    top = 3000 * counter;
                    var url = '/selected/?p=' + counter;

                    $.get(url, function (html) {
                        var $html = $(html);
                        $html.each(function () {
                            showEntityTitle($(this));
                        });
                        $html.appendTo($selection);
                    });
                }
            });
        }
    })();

    // 展开点评
    $('.selection-item').each(function () {
        showEntityTitle($(this));
    });

    function showEntityTitle($selectionItem) {
        var $entityTitle = $selectionItem.find('.entity .title');
        $selectionItem.hover(function () {
            $entityTitle.slideDown('fast');
        }, function () {
            $entityTitle.slideUp('fast');
        });
    }

    // 点评事件处理
    $('.note-item').each(function () {
        var $this = $(this);
        dealUpdateNote($this);
        addCommentEventHandle($this);
    });

    function toggleNote($selectionItem) {
        $selectionItem.find('.show-note').on('click', function () {
            var $commonNote = $selectionItem.find('.common-note');

            // 确保只加载1次
            if ($commonNote[0].hasChildNodes()) {
                $commonNote.slideToggle('slow');
            } else {
                var url = '/entity/' + $(this).attr('data-entity') + '/note/';
                $.get(url, function (data) {
                    $commonNote.html(data);
                    $commonNote.slideToggle('slow');

                    $commonNote.find('.note-item').each(function () {
                        var $this = $(this);
                        dealUpdateNote($this);
                        addCommentEventHandle($this);
                    })
                });
            }
        });
    }

    function dealUpdateNote($noteItem) {
        var $this = $noteItem;
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
    }

    // 评论
    function addCommentEventHandle($noteItem) {
        var $this = $noteItem;
        var $noteDetail = $this.find('.note-detail');

        $this.find('.add-comment').on('click', function () {
            var $noteComment = $this.find('.note-comment');

            if ($noteComment[0]) {
                $noteComment.slideToggle('fast');
            } else {
                var url = '/note/' + $(this).attr('data-note') + '/comment/';
                $.get(url, function (data) {
                    $noteComment = $(data);
                    $noteComment.appendTo($noteDetail);
                    addCommentEvent($noteComment);
                    $noteComment.slideToggle('fast');
                });
            }
        });
    }

    function addCommentEvent($noteComment) {
        var $form = $noteComment.find('form');
        var $commentText = $form.find('input[name="comment_text"]');
        var replyToUser = '';
        var replyToComment = '';

        $form.find('.cancel-comment').one('click', function () {
            $noteComment.slideUp('fast');

            replyToUser = '';
            replyToComment = '';
            $commentText.val('');
        });

        $noteComment.find('.reply').on('click', function () {
            var $parent = $(this).parent();
            var $p = $parent.find('.comment-content');
            var $nickname = $parent.find('.nickname');

            $commentText.val('回复 ' + $nickname.text() + ': ');
            $commentText.focus();
            replyToUser = $p.attr('data-creator');
            replyToComment = $p.attr('data-comment');
        });

        $noteComment.find('.close').on('click', function (e) {
            var $noteCommentItem = $(this).parent().parent();

            $.post(this.href, function (data) {
                if (parseInt(data) === 1) {
                    $noteCommentItem.remove();
                }
            });

            e.preventDefault();
        });

        $form.find('.operate-comment input').on('click', function (e) {
            var commentText = $.trim($commentText.val());

            commentText = commentText.replace(/^回复.*[:：]/, function (str, index) {
                if (index === 0) {
                    return '';
                }
                return str;
            });

            commentText = $.trim(commentText);

            if (commentText.length > 0) {
                var url = $form[0].action;
                var data = {
                    comment_text: commentText,
                    reply_to_user_id: replyToUser,
                    reply_to_comment_id: replyToComment
                };

                $.post(url, data, function (htmlData) {
                    $commentText.val('');
                    $(htmlData).insertBefore($form);

                    replyToUser = '';
                    replyToComment = '';
                });
            }

            e.preventDefault();
        });
    }

    // 点评 点赞
   function pokeEventHandle ($poke) {
        var $counter = $poke.find('small');
        var note_id = $poke.attr('data-note');
        var url = '/note/' + note_id + '/poke/';

        $.post(url, function (data) {
            var count = parseInt($counter.text());
            var result = parseInt(data);

            if (result === 1) {
                $counter.text(count + 1);
                $poke.addClass('already-poke');
            } else if (result === 0) {
                $counter.text(count - 1);
                $poke.removeClass('already-poke');
            }
        });
    }

    $('.poke').on('click', function () {
        pokeEventHandle($(this));
    });

    // 喜爱 like
    $('.like-entity').on('click', function () {
        var $this = $(this);
        var $counter = $this.find('small');
        var entity_id = $this.attr('data-entity');
        var url = '/entity/' + entity_id + '/like/';

        $.post(url, function (data) {
            var count = parseInt($counter.text());
            var result = parseInt(data);

            if (result === 1) {
                $counter.text(count + 1);
                $this.addClass('already-like-entity');
            } else if (result === 0) {
                $counter.text(count - 1);
                $this.removeClass('already-like-entity');
            }
        });
    });

    // 关注
    $('.follow-user').on('click', function () {
        var $this = $(this);
        var user_id = $this.attr('data-user');
        var url = '/u/' + user_id + '/follow/';

        $.post(url, function (data) {
            var result = parseInt(data);

            if (result === 1) {
                $this.text('取消关注');
            } else if (result === 0) {
                $this.html('<span></span> 关注');
            }
        });
    });

    // header user hover
    $('#header').find('.user .container').hover(function () {
        var $this = $(this);
        var $pop = $this.find('.pop');
        var $small = $this.find('small');

        $this.addClass('container-hover');
        $small.addClass('hover');
        $pop.show();
    }, function () {
        var $this = $(this);
        var $pop = $this.find('.pop');
        var $small = $this.find('small');

        $this.removeClass('container-hover');
        $pop.hide();
        $small.removeClass('hover');
    });

    // user center
    $('#user-center').find('.entity-nav .filter').hover(function () {
        $(this).find('.price').css('display', 'block');
    }, function () {
        $(this).find('.price').hide();
    });

    // 添加商品
    var $addEntity = $('#add-entity');

    $addEntity.find('.brand input').on('change', function () {
        $('#entity-brand')[0].value = this.value;
    });

    $addEntity.find('.title input').on('change', function () {
        $('#entity-title')[0].value = this.value;
    });

    $addEntity.find('.detail-img img').on('click', function () {
        $('#entity-img-url')[0].value = this.src;
        $addEntity.find('.img-container img')[0].src = this.src;
    });

})(jQuery, document, window);