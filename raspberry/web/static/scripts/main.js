/**
 * Created by cuiwei on 13-12-26.
 */
;(function ($, document, window) {
    // 动态加载selection
    (function () {
        var $selection = $('#selection');
        if ($selection[0]) {
            var counter = 1;
            var top = 3000;

            $(window).scroll(function () {
                var $this = $(this);

                if ($this.scrollTop() > top) {
                    counter++;
                    top += 2300;
                    var url = '/selected/?p=' + counter;

                    $.get(url, function (result) {
                        result = $.parseJSON(result);
                        var status = parseInt(result.status);

                        if (status === 1) {
                            var $html = $(result.data);
                            $html.each(function () {
                                showEntityTitle($(this));
                            });
                            $html.appendTo($selection);
                        } else if (status === 0) {
                            // 没有数据可以加载了
                        }
                    });
                }
            });
        }
    })();

    // 为精选添加 鼠标悬浮显示标题
    $('.selection-item').each(function () {
        showEntityTitle($(this));
    });

    function showEntityTitle($selectionItem) {
        // 为精选添加 鼠标悬浮显示标题

        var $entityTitle = $selectionItem.find('.entity .title');
        $selectionItem.hover(function () {
            $entityTitle.slideDown('fast');
        }, function () {
            $entityTitle.slideUp('fast');
        });
    }


    // 写点评
    $('.add-note').each(function () {
        var $this = $(this);
        var $notes = $this.parent().find('.notes');
        var $form = $this.find('form');
        var $textarea = $this.find('textarea');

        $textarea.on({
            focus: function () {
                // TODO 先判断是否登录
                $form.addClass('active');
            }
        });

        $form.find('.cancel').on('click', function () {
            $form.removeClass('active');
        });

        $form.on('submit', function (e) {
            var textarea = $textarea[0];

            if ($.trim(textarea.value).length === 0) {
                textarea.value = '';
                textarea.focus();
            } else {
                $.post(this.action, $form.serialize(), function (result) {
                    result = $.parseJSON(result);
                    var status = parseInt(result.status);

                    if (status === 1) {
                        var $html = $(result.data);
                        updateNote($html);
                        clickComment($html);

                        $('<div class="sep"></div>').appendTo($notes);
                        $html.appendTo($notes);

                        $this.remove();
                    } else if (status === 0) {
                        // error
                    }
                });
            }
            e.preventDefault();
        });
    });

    // 点评事件处理
    $('.note-item').each(function () {
        var $this = $(this);
        updateNote($this);
        clickComment($this);
    });

    function updateNote($noteItem) {
        // 用于修改点评，为修改点评按钮添加事件处理等

        var $form = $noteItem.find('.update-note-form');

        if ($form[0]) {
            var $textarea = $form.find('textarea');
            var textarea = $textarea[0];
            var $noteContent = $noteItem.find('.note-content');
            var originNoteText;

            $noteItem.find('.update-note').on('click', function () {
                originNoteText = textarea.value;
                $noteContent.hide();
                $form.show();
            });

            $form.find('.cancel').on('click', function () {
                textarea.value = originNoteText;
                $form.hide();
                $noteContent.show();
            });

            $form.on('submit', function (e) {
                var noteText = textarea.value;

                if (noteText !== originNoteText && noteText.length > 0) {
                    $.post($form[0].action, $form.serialize(), function (data) {
                        if (parseInt(data) === 1) {
                            $noteContent.text(noteText);
                            $form.hide();
                            $noteContent.show();
                        }
                    });
                }

                e.preventDefault();
            });
        }
    }

    function clickComment($noteItem) {
        // 点击 为点评添加评论时候 的事件处理

        var $noteDetail = $noteItem.find('.note-detail');

        // 动态加载点评
        $noteItem.find('.add-comment').on('click', function () {
            var $noteComment = $noteItem.find('.note-comment');

            if ($noteComment[0]) {
                $noteComment.slideToggle('fast');
            } else {
                var url = '/note/' + $(this).attr('data-note') + '/comment/';

                $.get(url, function (result) {
                    result = $.parseJSON(result);
                    var status = parseInt(result.status);

                    if (status === 1) {
                        var $html = $(result.data);

                        comment($html);
                        $html.appendTo($noteDetail);
                        $html.slideToggle('fast');
                    } else if (status === 0) {
                        // error
                    }
                });
            }
        });
    }

    function comment($noteComment) {
        // 用于添加点评时候的事件处理

        var $form = $noteComment.find('form');
        var $commentText = $form.find('.text');
        var replyToUser = '';
        var replyToComment = '';

        $form.find('.cancel-comment').on('click', function () {
            $noteComment.slideUp('fast');

            replyToUser = '';
            replyToComment = '';
            $commentText.val('');
        });

        function reply($commentItem) {
            $commentItem.find('.reply').on('click', function () {
                var $commentContent = $commentItem.find('.comment-content');
                var $nickname = $commentItem.find('.nickname');

                $commentText.val('回复 ' + $nickname.text() + ': ');
                $commentText.focus();
                replyToUser = $commentContent.attr('data-creator');
                replyToComment = $commentContent.attr('data-comment');
            });

            $commentItem.find('.close').on('click', function (e) {
                $.post(this.href, function (data) {
                    if (parseInt(data) === 1) {
                        $commentItem.remove();
                    }
                });

                e.preventDefault();
            });
        }

        $noteComment.find('.note-comment-item').each(function () {
            reply($(this));
        });

        $form.on('submit', function (e) {
            var input = $commentText[0];
            var text = $.trim(input.value);

            text = text.replace(/^回复.*[:：]/, function (str, index) {
                if (index === 0) {
                    return '';
                }
                return str;
            });
            text = $.trim(text);

            if (text.length > 0) {
                var url = $form[0].action;
                var data = {
                    comment_text: text,
                    reply_to_user_id: replyToUser,
                    reply_to_comment_id: replyToComment
                };

                $.post(url, data, function (result) {
                    result = $.parseJSON(result);
                    var status = parseInt(result.status);

                    if (status === 1) {
                        var $html = $(result.data);
                        reply($html);

                        $html.insertBefore($form);
                    } else {
                        // error
                    }

                    input.value = '';
                    replyToUser = '';
                    replyToComment = '';
                });
            } else {
                input.value = '';
                input.focus();
            }

            e.preventDefault();
        });
    }

    // 点评 点赞
    $('.poke').on('click', function () {
        poke($(this));
    });

    function poke($poke) {
        // 点评 点赞

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

    // 喜爱 like
    $('.like').on('click', function (e) {
        e.preventDefault();
        like($(this));
    });

    function like($like) {
        // 喜爱 like entity

        var $counter = $like.find('.count');

        $.post($like[0].href, function (data) {
            var count = parseInt($counter.text());
            var result = parseInt(data);

            if (result === 1) {
                $counter.text(count + 1);
                $like.addClass('liked');
            } else if (result === 0) {
                $counter.text(count - 1);
                $like.removeClass('liked');
            }
        });
    }

    $('#detail').each(function () {
        // 鼠标放细节图上后效果

        var $this = $(this);
        $this.find('.detail-img img').on('mouseover', function () {
            $this.find('.entity-img img')[0].src = this.src;
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