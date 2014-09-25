/**
 * Created by edison on 14-9-21.
 */

;(function ($, document, window) {


    var util = {
        like: function () {
            // 喜爱 like entity
            $('.btn-like, .btn-like-detail').live('click', function (e) {
                var like = $(this);
                var counter = like.find('.like-count');
                var url = $(this).attr("href");
                var heart = like.find("i");
                var status = 0;
                if (heart.hasClass("fa-heart-o")) {
                    status = 1;
                }
                url = url.replace(/\/[01]\//,"/"+status+"/");
                $.post(url, function(data){
                    var count = parseInt(counter.text());
                    var result = parseInt(data);
//                    console.log(result);
                    if (result === 1) {
                        counter.text(" "+(count + 1));
                        heart.removeClass('fa-heart-o');
                        heart.addClass('fa-heart');
                    } else if (result === 0) {
                        counter.text(" "+(count - 1));
                        heart.removeClass('fa-heart');
                        heart.addClass('fa-heart-o');
                    }
                });
                e.preventDefault();
            });
        }
    };

    var selection = {
        loadData: function () {

            var $selection = $('#selection');
//            console.log($selection);
            if ($selection) {
                var counter = 1;
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

                    //这里临时不采用自动加载，换成分页
                    if (($(window).height() + $(window).scrollTop()) >= $(document).height() && flag == false) {
//                        console.log("okokokokoko");
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
//                    return data;
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

            $('.share a').live('click', function(e){
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
            $cancel.live('click', function() {
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
        }
    };

    (function init() {

        util.like();

        selection.loadData();

        detail.detailImageHover();
        detail.shareWeibo();
        detail.postNote();
    })();


})(jQuery, document, window);