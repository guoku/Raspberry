/**
 * Created by edison on 14-9-21.
 */

;(function ($, document, window) {


    var util = {
        modalSignIn: function(html) {
            var signModal = $('#SignInModal');
            var signContent = signModal.find('.modal-content');
            if (signContent.find('.row')[0]) {
                signModal.modal('show');
            } else {
                html.appendTo(signContent);
                signModal.modal('show');
            }
        },


        like: function () {
            // 喜爱 like entity
            $('.btn-like, .btn-like-detail').on('click', function (e) {
                var like = $(this);
                var counter = like.find('.like-count');
                var url = $(this).attr("href");
                var heart = like.find("i");
                var status = 0;
                if (heart.hasClass("fa-heart-o")) {
                    status = 1;
                }
                url = url.replace(/\/[01]\//,"/"+status+"/");
//                console.log(url);
                $.ajax({
                    url: url,
                    type: 'POST',
                    success: function(data) {
                        var count = parseInt(counter.text());
                        var result = parseInt(data);
                        if (result === 1) {
                            counter.text(" "+(count + 1));
                            heart.removeClass('fa-heart-o');
                            heart.addClass('fa-heart');
                        } else if (result === 0){
//                            console.log(result);
                            if (count >0) {
                                counter.text(" " + (count - 1));
                                heart.removeClass('fa-heart');
                                heart.addClass('fa-heart-o');
                            }
                        } else {
                            var html = $(data);
                            util.modalSignIn(html);
                        }
                    }
                });
                e.preventDefault();
            });
        },

        createEntity: function () {
            var form = $('.create-entity form');
            var entityExist = $(".entity-exist");
            var addEntity = $(".add-entity");
            var imageThumbails = $(".image-thumbnails");
//            console.log(entityExist);
            form.on('submit', function(e) {
                var entity_url = form.find("input[name='cand_url']").val();
//                console.log(this.action);
                $.ajax({
                    type: 'post',
                    url: this.action,
                    data: {cand_url:entity_url},
                    dataType:"json",
                    success : function (data) {
                        if(data.status == "EXIST") {
                            entityExist.find('a').attr("href", "/detail/"+data.data.entity_hash);
                            entityExist.slideDown();
                        } else {
                            entityExist.slideUp();
                            if (data.data.taobao_id == undefined) {

                            } else {
                                $(".detail_title span:eq(1)").text(data.data.taobao_title);
//                                $(".detail_title_input").val(data.data.taobao_title);
                                var title = $.trim(data.data.taobao_title);
                                addEntity.find(".title").text(title);
                                addEntity.find("input[name=title]").val(title);
                            }
                            addEntity.find(".entity-chief-img").attr('src', data.data.chief_image_url);
                            imageThumbails.html("");
                            for(var i=0; i < data.data.thumb_images.length; i++) {
                                console.log(data.data.thumb_images[i]);
                                var fix = data.data.taobao_id == undefined ? "" : "_50x50.jpg";
                                imageThumbails.append("<div class='col-xs-3 col-sm-2'><div class='thumbnail'><div class='img-box'><img class='img-responsive' src="
                                    +data.data.thumb_images[i]+fix+"></div></div></div>");
                            }
                            addEntity.slideDown();
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });
        }
    };

    var selection = {
        loadData: function () {

            var $selection = $('#selection');
            var page = $selection.parent().find('.pager');
            var counter = 1;
            page.hide();

            if ($selection[0]) {
                var flag = false;
//                console.log(counter);
                $(window).scroll(function () {
                    if($(window).scrollTop()>100){
//                        if($(".click_to_top").css("display") == "none"){
//                            clickToTop.caculateRight();
//                            $(".click_to_top").fadeIn();
//                        }
                    }else{
//                        if($(".click_to_top").css("display") == "block")
//                        $(".click_to_top").fadeOut();
                    }

                    if (counter % 3 == 0 ) {
                        page.show();
                    } else {
                        page.hide();
                    }
                    //这里临时不采用自动加载，换成分页
                    if (($(window).height() + $(window).scrollTop()) >= $(document).height() && flag == false && counter % 3 != 0) {
//                        console.log("okokokokoko");
//                        page.hide();
                        flag = true;
                        var url = window.location.href;
//                        var time = $(".common-note:last").find(".timestr").attr("name");
//                        var time = $selection.find().attr("name");
                        var last_entity = $selection.find('.entity-selection:last');
                        var time = last_entity.find(".timestr").attr("name");
//                        console.log(time);
                        $.ajax({
                            url: url,
                            type: "GET",
                            data: {'p': counter,'t':time},
                            success: function(data) {
                                result =  $.parseJSON(data);
                                var status = parseInt(result.status);
                                if (status === 1) {
                                    var $html = $(result.data);
//                                    $html.each(function () {
//                                        util.showEntityTitle($(this));
//                                    });
                                    $html.appendTo($selection);
                                    counter ++;
                                    flag = false;
                                }
                            }
                        });
                    }
                });
            }
//            var entities = $selection.find('.entity-selection');
//            console.log(entities);
        }
    };

    var detail = {

        detailImageHover: function () {
            // 鼠标放细节图上后效果

            $('#detail').each(function () {
                var $this = $(this);
                $this.find('.detail-img img').on('mouseover', function () {
//                    console.log(this);
                    var re = /64x64/;
                    var url_string = this.src.replace(re, '640x640');
                    $this.find('.entity-detail img')[0].src = url_string;
                });
            });
        },

        shareWeibo: function() {
//            var self = this;

            $('.detail-share a').on('click', function(e){
                e.preventDefault();

                var url = location.href;
//                console.log(url);
                var pic = $('.entity-detail img').attr("src");
//                console.log(pic);
                var content = $('.selection-note .note-text .content').html();
//                console.log(content);
                content = content.replace(/<[\s\S]*?>/g, "");
                content = content.replace(/%/, "");
                content = content.replace(/&nbsp;/, "");
//                console.log(content);
                var param = {
                    url:url,
                    type:'3',
                    count:'0',
                    appkey:'1459383851',
                    title:content,
                    pic:pic,
                    ralateUid:'2179686555',
                    rnd:new Date().valueOf()
                };
                var temp = [];
                for( var p in param ){
                    temp.push(p + '=' + encodeURIComponent( param[p] || '' ) )
                }
                var link = "http://service.weibo.com/share/share.php?" + temp.join('&');
                window.open(link);
            });
        },

        postNote: function () {
            var $note = $(".post-note");
            var $form = $note.find("form");
            var $textarea = $form.find("textarea");
//            console.log($textarea);

            $textarea.on('focus', function(){
//
                $form.addClass('active');
            });
//console.log($note);

            var $cancel = $form.find('.btn-cancel');
//                console.log($cancel);
            $cancel.on('click', function() {
//                console.log(this);
                $form.removeClass('active');
            });

            $form.on('submit', function (e) {
                if ($.trim($textarea.value).length === 0) {
                    $textarea.value = '';
                    $textarea.focus();
                } else {
                    $.post(this.action, $form.serialize(), function (result){
                        result = $.parseJSON(result);
                        var status = parseInt(result.status);
                        if (status === 1) {
                            var $html = $(result.data);
//                            self.updateNote($html);
//                            self.clickComment($html);
//                            self.poke();
//                            $('<div class="sep"></div>').appendTo($notes);
//                            $html.appendTo($notes);

                            $note.remove();
                        } else if (status === 0) {
                            // error
                        }
                    });
                }

//                console.log("OKOKOKO");
                 e.preventDefault();
            });
        },

        noteAction: function () {

            var noteDetail = $(".selection-note, .common-note-item");
            noteDetail.each(function(){
//                var $this = $(this);
                detail.clickComment($(this));
            });
        },

        commentAction: function(comment) {
            var form = comment.find('form');
            var commentText = form.find('input');
            var replyToUser = '';
            var replyToComment = '';

            comment.find('.btn-cancel').on('click', function() {
//                console.log(comment);
                comment.slideToggle('fast');
                commentText.val('');
            });

            function reply(commentItem) {
//                console.log(commentItem.find('.reply'));
                commentItem.find('.reply').on('click', function (e) {
//                    e.preventDefault();
//                    if (!util.isUserLogined()) {
//                        util.popLoginBox();
//                    } else {

                    var commentContent = commentItem.find('.comment-content');
                    var nickname = commentItem.find('.nickname');
//                    console.log(nickname);
                    commentText.val('回复 ' + $.trim(nickname.text()) + ': ');
                    commentText.focus();
                    replyToUser = commentContent.attr('data-creator');
                    replyToComment = commentContent.attr('data-comment');
//                    }
                    return false;
                });

                commentItem.find('.close').on('click', function (e) {
                    $.post(this.href, function (data) {
                        if (parseInt(data) === 1) {
                            commentItem.remove();
                        }
                    });

                    return false;
                });
            }

            comment.find('.media').each(function () {
                reply($(this));
            });

//            var commentItem = commentItem;
            form.on('submit', function(e) {
                var input = commentText[0];
                var text = input.value;

                text = text.replace(/^回复.*[:：]/, function (str, index) {
                    if (index === 0) {
                        return '';
                    }
                    return str;
                });
                text = $.trim(text);
                if (text.length > 0) {
                    var url = form[0].action;
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

                            $html.insertBefore(form);
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
        },

        clickComment: function (note) {


//            console.log(noteDetail);
//            console.log(note);
            note.find('.add-comment').on('click', function (e) {
                var comments = note.find('.note-comment-list');
                var notecontent = note.find(".note-content");
//                console.log(notecontent);
                if(comments[0]) {
                    comments.slideToggle('fast');
                } else {

                    var url = '/note/' + $(this).attr('data-note') + '/comment/';
//                    console.log(url);
                    $.ajax({
                        url: url,
                        type: 'GET',
//                        async: false,
                        success: function(data){
                            result =  $.parseJSON(data);
                            var $html = $(result.data);
//                            self.noteComment($html);
                            detail.commentAction($html);
                            $html.appendTo(notecontent);
                            $html.slideToggle('fast');
//                            initTag();
                        },
                        error: function(ajaxContext) {
                             console.log(ajaxContext['responseText']);
//                            if (!util.isUserLogined()) {
//                                util.popLoginBox();
//                            } else {
////                                console.log(ajaxContext['responseText']);
//                                result =  $.parseJSON(ajaxContext['responseText']);
//                                var $html = $(result.data);
//                                self.noteComment($html);
//                                $html.appendTo($noteDetail);
//                                $html.slideToggle('fast');
//                                initTag();
//                            }
//                            alert(ajaxContext.responseText);
                        }
                    });
                    return false;
                }
            });
        }
    };

    (function init() {

        util.like();
        util.createEntity();
        selection.loadData();

        detail.detailImageHover();
        detail.shareWeibo();
        detail.postNote();
        detail.noteAction();
    })();


})(jQuery, document, window);