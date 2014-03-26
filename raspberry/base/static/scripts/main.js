/**
 * Created by cuiwei on 13-12-26.
 */
function initTag(){
    var array = $(".with-tag");
    for (var i=0; i<array.length; i++) {
        var str = array.eq(i).html(array.eq(i).html().replace(/\<br[!>]*\>/g, "\n")).text();
        if (str == undefined)
            continue;

        var ereg = /[#＃][0-9a-zA-Z\u4e00-\u9fff\u3040-\u30FF\u30A0-\u30FF]+/g;
        var cut = str.match(ereg);
        if (cut == null){
            array.eq(i).html(str.replace(/\n/g, "<br>"));
            continue;
        }
            
        for (var j in cut){
            str = str.replace(cut[j], "<a class='tag_display' rel='nofollow' href='/tag/"+encodeURI(cut[j].replace(/[#＃]/,""))+"' >"+cut[j]+"</a>&nbsp;");
        }

        array.eq(i).html(str.replace(/\n/g, "<br>"));
    }
}

;(function ($, document, window) {
    $.fn.TagAC = function (){
        var pos, tag, cursor, length, timeout,
            start = -1,
            ereg = /^[0-9a-zA-Z\u4e00-\u9fff\u3040-\u30FF\u30A0-\u30FF]*$/,
            dom = $('<div class="tag-auto-complete"><span>选择 # 标记或直接输入</span></div>');
        function init(){
            tag = "";
            cursor = -1;
            length = 0;
//            $("textarea[name='note_text']").css("height","20px");
            dom.css("margin", "0");

            clearTimeout(timeout);

            $(".tag-auto-complete, .text_area").hide();
        }
        function getRes(obj, word, callback){
            var word = word || "";
            var callback = callback || function(){};

            var url = "/tag/suggest/";
            if (word) {
                if (!ereg.test(word)){
                    init();
                    return false;
                }

                url = url + "?prefix=" + word;
                dom.find("span").text();
            }
            $.post(url, {}, function(xhr){
                dom.find("p").remove();

                if (xhr == "[]"){
                    dom.find("span").text("轻敲空格完成输入");
                }
                else {
                    dom.find("span").text("选择 # 标记或直接输入");
                    var arr = eval(xhr);
                    for(var i in arr){
                        dom.append("<p># " + arr[i] + "</p>");
                    }
                    dom.find("p:first").addClass("hover");
                }

                callback();

                dom.css("margin-left", pos.left-5).css("margin-top", pos.top+15);
                dom.show();
                dom.find("p").mouseover(function(){
                    dom.find("p").removeClass("hover");
                    $(this).addClass("hover");
                }).click(function(e){
                    var text = $(this).text().replace("# ", "");
                    var front = obj.val().slice(0, start);
                    var back = obj.val().slice(cursor);
                    obj.val(front + text + " " + back);

                    init();
                    e.preventDefault();
                });
            });
        }
        
        init();

        return this.live("keyup", function(e){
            var obj = $(this);
            var e = e||window.event;
            var code = e.which;
            cursor = e.target.selectionEnd;

            if (code == 51 && e.shiftKey){
                init();
                start = e.target.selectionEnd;
                length = obj.val().length;

                var div_text = $('<div class="text_area"></div>');
                obj.after(div_text);
                div_text.html(obj.val().slice(0,start).replace(/\n/g, "<br>").replace(/\s/g, "&nbsp;") + "<span class='pos'>&nbsp;</span>");

                pos = div_text.find(".pos").position();

                getRes(obj, tag, function(){
                    if (obj.parent().find(".tag-auto-complete").get(0) == undefined)
                        obj.after(dom);
                })
            }
            else if (start >= 0 && length != obj.val().length && !(code > 36 && code < 41) ){
                clearTimeout(timeout);
                length = obj.val().length;
                tag = obj.val().slice(start, cursor);

                timeout = setTimeout( function(){getRes(obj, tag);}, 300);
            }

        }).live("keydown", function(e){
            if (start < 0)
                return true;

            var obj = $(this);
            var e = e||window.event;
            var code = e.which;
            cursor = e.target.selectionEnd;

            if (code == 8){
                if (start == cursor){
                    init();
                    start = -1;
                }
            }
            else if (code == 27){
                obj.blur();
            }
            else if (code == 13){
                if (dom.css("display") == "none")
                    return true;
                var cur = dom.find("p.hover");
                cur.click();
                e.preventDefault();
            }
            else if (code == 38){
                if (dom.css("display") == "none")
                    return true;

                var cur = dom.find("p.hover");
                if (cur.get(0) == dom.find("p:first").get(0) ){
                    dom.find("p:last").mouseover();
                }
                else {
                    cur.prev().mouseover();
                }
                e.preventDefault();
            }
            else if (code == 40){
                if (dom.css("display") == "none")
                    return true;

                var cur = dom.find("p.hover");
                if (cur.get(0) == dom.find("p:last").get(0) ){
                    dom.find("p:first").mouseover();
                }
                else {
                    cur.next().mouseover();
                }
                e.preventDefault();
            }
            else if (code == 37){
                clearTimeout(timeout);
                if (cursor-1 < start) {
                    dom.hide();
                    return true;
                }
                tag = obj.val().slice(start, cursor-1);
                timeout = setTimeout( function(){getRes(obj, tag);}, 300);
            }
            else if (code == 39){
                clearTimeout(timeout);
                if (cursor+1 >= start) {
                    tag = obj.val().slice(start, cursor+1);
                    timeout = setTimeout( function(){getRes(obj, tag);}, 300);
                }
            }
            
        }).on("blur", function(){
            //init();
        });
    };

    var util = {
        isUserLogined: function () {
            // 通过前端简单检测用户是否登录，该方法是不可靠的，后端仍需要检测限制
            // 除非用户特意更改，否则足以检测，就算更改，后端也会判断的

            return !!$('#header').find('.user-avatar')[0];
        },

        popLoginBox: function () {
            var $accountForm = $('.account-form');
            var $overlay = $('.overlay');
            var $login = $('.account-form.login');
            var $reg =  $('.account-form.register');
            $accountForm.on('click', formClick);
            function formClick(e) {
                e.stopPropagation();
            }
            var flag = 1;
            var $body = $('body');
            $overlay.show();
            $login.show();
            $body.addClass('overlay-open');
            $body.on('click', removeLogin);
            function removeLogin() {
                if (flag == 1) {
                    $overlay.hide();
                    $accountForm.hide();
                    $body.removeClass('overlay-open');
                    $body.off('click', removeLogin);
                    $accountForm.off('click', formClick);
                }
                flag = 1;
            }
            
            $login.find('.to-reg').on('click', function (e) {
                
                $login.hide();
                $reg.show();
                e.preventDefault();
            });

            $reg.find('.to-login').on('click', function (e) {
                
                $reg.hide();
                $login.show();
                e.preventDefault();
            });
        },

        like: function () {
            // 喜爱 like entity
            var self = this;
            $('.like').live('click', function (e) {
                if (!self.isUserLogined()) {
                    self.popLoginBox();
                } else {
                    var $like = $(this);
                    var $counter = $like.find('.count');
                    var url = $(this).attr("href");
                    if(url[url.length-2] == 1)
                    	var like_status = 0;
                    else
                    	var like_status = 1;
                   	var s = url.replace(/\/[01]\//,"/"+like_status+"/");
                   	$(this).attr("href",s);
                    $.post(url, function (data) {
                        var count = parseInt($counter.text());
                        var result = parseInt(data);

                        if (result === 1) {
                            $counter.text(" "+(count + 1));
                            $like.addClass('liked');
                        } else if (result === 0) {
                            $counter.text(" "+(count - 1));
                            $like.removeClass('liked');
                        }
                    });
                }

                e.preventDefault();
            });
        },
        showEntityTitle: function ($noteItem) {
            // 为精选添加 鼠标悬浮显示标题

            var $entityTitle = $noteItem.find('.title');
            $noteItem.hover(function () {
                $entityTitle.slideDown('fast');
            }, function () {
                $entityTitle.slideUp('fast');
            });
        },

        noteHover: function () {
            var self = this;
            $('.common-note, .popular-entity, .common-entity').each(function () {
                self.showEntityTitle($(this));
            });
        },

        loadData: function(counter, object) {
            var url = window.location.href;
            $.ajax({
                url: url,
                type: "GET",
                async: false,
                data: {'p': counter },
                success: function(data) {
//                    return data;
                    result =  $.parseJSON(data);
                    var status = parseInt(result.status);
                    if (status === 1) {
                        var $html = $(result.data);
                        $html.each(function () {
                            util.showEntityTitle($(this));
                        });
                        $html.appendTo(object);
                    }
                }
            });
        },

        shareWeibo: function() {
//            var self = this;

            $('.share a').live('click', function(e){
//                console.log(this);
                e.preventDefault();

                var url = location.href;
//                console.log(url);
                var pic = $('.entity-img img').attr("src");
                var content = $('.selection-note .note-item .note-detail p').html();
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
        }
    };

    var selection = {
        loadSelections: function () {
            // 动态加载selection

            var $selection = $('.selections');

            if ($selection[0]) {
                var counter = 1;
//                var top = 3000;

                $(window).scroll(function () {
                    if($(window).scrollTop()>100){
                        if($(".click_to_top").css("display") == "none"){
                            clickToTop.caculateRight();
                            $(".click_to_top").fadeIn();
                        }
                    }else{
                        if($(".click_to_top").css("display") == "block")
                        $(".click_to_top").fadeOut();
                    }
                    var $this = $(this);
                    
                    //这里临时不采用自动加载，换成分页
                    if (($(window).height() + $(window).scrollTop()) >= $(document).height()) {
                            
//                    if ($this.scrollTop() > top) {
                        counter++;
                        util.loadData(counter, $selection);
                    }
                });
            }
        }
    };

//    var category = {
//        loadCategory: function () {
//            var $category = $('.category');
//            if ($category[0]) {
//                var counter = 1;
//                var top = 3000;
//
//                $(window).scroll(function () {
//                    var $this = $(this);
////                    console.log($this);
//                });
//            }
//        }
//    };

    var detail = {
        updateNote: function ($noteItem) {
            // 用于修改点评，为修改点评按钮添加事件处理等
            var $form = $noteItem.find('.update-note-form');

            if ($form[0]) {
                var $textarea = $form.find('textarea');
                var textarea = $textarea[0];
                var $noteContent = $noteItem.find('.note-content');
                var originNoteText;

                $textarea.TagAC();

                $noteItem.find('.update-note').on('click', function () {
                	if($form.css("display")=="block"){
                		$form.find(".cancel").click();
                		return ;
                	}
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
        },

        noteComment: function ($noteComment) {
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
                $commentItem.find('.reply').live('click', function (e) {
//                    e.preventDefault();
                    if (!util.isUserLogined()) {
                        util.popLoginBox();
                    } else {

                        var $commentContent = $commentItem.find('.comment-content');
                        var $nickname = $commentItem.find('.nickname');

                        $commentText.val('回复 ' + $.trim($nickname.text()) + ': ');
                        $commentText.focus();
                        replyToUser = $commentContent.attr('data-creator');
                        replyToComment = $commentContent.attr('data-comment');
                    }
                    return false;
                });

                $commentItem.find('.close').live('click', function (e) {
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
        },

        clickComment: function ($noteItem) {
            // 点击 为点评添加评论时候 的事件处理


            $(".note-comment input.text").TagAC();
            var self = this;
            var $noteDetail = $noteItem.find('.note-detail');

            // 动态加载点评的评论
            $noteItem.find('.add-comment').live('click', function (e) {
//                e.preventDefault();
                var $noteComment = $noteItem.find('.note-comment');
                if ($noteComment[0]) {
                    $noteComment.slideToggle('fast');
                } else {
                    var url = '/note/' + $(this).attr('data-note') + '/comment/';
                    $.ajax({
                        url: url,
                        type: 'GET',
                        async: false,
                        success: function(data){
                            result =  $.parseJSON(data);
                            var $html = $(result.data);
                            self.noteComment($html);
                            $html.appendTo($noteDetail);
                            $html.slideToggle('fast');
                            initTag();
                        },
                        error: function(ajaxContext) {
                            if (!util.isUserLogined()) {
                                util.popLoginBox();
                            } else {
//                                console.log(ajaxContext['responseText']);
                                result =  $.parseJSON(ajaxContext['responseText']);
                                var $html = $(result.data);
                                self.noteComment($html);
                                $html.appendTo($noteDetail);
                                $html.slideToggle('fast');
                                initTag();
                            }
//                            alert(ajaxContext.responseText);
                        }
                    });
                    return false;
                }
            });
        },

        detailImageHover: function () {
            // 鼠标放细节图上后效果

            $('#detail').each(function () {
                var $this = $(this);
                $this.find('.detail-img img').on('mouseover', function () {
                    var re = /64x64/;
                    var urlstr = this.src.replace(re, '640x640');
                    $this.find('.entity-img img')[0].src = urlstr;
                });
            });
        },

        noteItem: function () {
            // 点评事件处理

            var self = this;

            $('.note-item').each(function () {
                var $this = $(this);
                self.updateNote($this);
                self.clickComment($this);
            });
        },

        addNote: function () {
            
            var self = this;
            var $addNote = $('.add-note-submit');
            var $notes = $addNote.parent().find('.notes');
            var $form = $addNote.find('form');
            var $textarea = $addNote.find('textarea');

            $textarea.on('click', function () {
                if (!util.isUserLogined()) {
                    util.popLoginBox();
                } else {
                    $form.addClass('active');
                }
            });
                
            $textarea.TagAC();

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
                            self.updateNote($html);
                            self.clickComment($html);
                            self.poke();
                            $('<div class="sep"></div>').appendTo($notes);
                            $html.appendTo($notes);

                            $addNote.remove();
                        } else if (status === 0) {
                            // error
                        }
                    });
                }
                e.preventDefault();
            });
        },

        poke: function () {
            // 点评 点赞
            $('.poke').live('click', function (e) {
                var $this = $(this);

                if (!util.isUserLogined()) {
                    util.popLoginBox();
                } else {
                    var $poke = $(this);
                    var $counter = $poke.find('small');
                    var note_id = $poke.attr('data-note');
                    var url = '/note/' + note_id + '/poke/';
                    if($this.attr("data-target-status") == 1){
                    	$this.attr("data-target-status",0);
                    	$poke.addClass('poked');
                        url+="1/";
                    }else{
                    	$poke.removeClass('poked');
                    	$this.attr("data-target-status",1);
                        url+="0/";
                    }
                    $.post(url, function (data) {
                        var count = parseInt($counter.text()) || 0;
                        var result = parseInt(data);

                        if (result === 1) {
                            count++;
                            $counter.text(count);
                            $poke.addClass('poked');

                            if (count === 1) {
                                $('<small>' + count + '</small>').appendTo($this);
                            }
                        } else if (result === 0) {
                            count--;
                            $counter.text(count);
                            $poke.removeClass('poked');

                            if (count === 0) {
                                $this.find('small').remove();
                            }
                        }
                    });
                }
                return false;
                e.preventDefault();
            });
        }
    };

    var user = {
        follow: function () {
            // 关注
            $('.follow-user').on('click', function (e) {
                var $this = $(this);

                $.post(this.href, function (data) {
                    var result = parseInt(data);

                    if (result === 1) {
                        if($this.hasClass(".is-fan")){
                            $this.html('<span class="img_is_fun"></span><b>取消关注</b>');
                        }else{
                            $this.html('<span class="img_not_fun"></span><b>取消关注</b>');
                        }
                        $this.removeClass("blue-f").addClass("gray-f");
                    } else if (result === 0) {
                        $this.html('<span class="img_follow"></span><b>关注</b>');
                        $this.removeClass("gray-f").addClass("blue-f");
                    }
                });

                e.preventDefault();
            });
        },

        priceFilterHover: function () {
            // user center
            $('#user-center').find('.user-like .prices').hover(function () {
                $(this).find('.price').css('display', 'block');
            }, function () {
                $(this).find('.price').hide();
            });
        }
    };

    var entity = {
        addEntity: function () {
            // 添加商品
            var $addEntity = $('#add-entity');

            $addEntity.find('.brand input').on('change', function () {
                $('#entity-brand')[0].value = this.value;
            });

            $addEntity.find('.title input').on('change', function () {
                $('#entity-title')[0].value = this.value;
            });

            // 切换图片
            $addEntity.find('.detail-img img').on('click', function () {
                $('#entity-img-url')[0].value = this.src;
                $addEntity.find('.img-container img')[0].src = this.src;
            });
        }
    };

    var clickToTop = {
        caculateRight:function(){
            if($("#selection").size()>0){
                var right = $("#selection").offset().left+$("#selection").width();
                $(".click_to_top").css("left",right+10);
            }
        },
        bindClick:function(){
            $(".click_to_top").click(function(){
                $("body,html").animate({
                    scrollTop:0,
                },500);
            });
        }
    };

    (function init() {
        util.like();
        util.noteHover();
//        util.popularHover();
        util.shareWeibo();

        clickToTop.caculateRight();
        clickToTop.bindClick();

        selection.loadSelections();
        //category.loadCategory();

        detail.detailImageHover();
        detail.addNote();
        initTag();
        detail.noteItem();
        detail.poke();

        user.follow();
        user.priceFilterHover();

        entity.addEntity();
    })();

})(jQuery, document, window);
$(function(){
	$(".account-form input[name='password'],.account-form input[name='email']").on("keyup",function(){
		if($(".account-form input[name='password']").val()!="" && $.trim($(".account-form input[name='email']").val())!=""){
			$(".account-form input[type='submit']").removeAttr("disabled").removeClass("submit_disabled").addClass("submit");
		}else{
			$(".account-form input[type='submit']").attr("disabled",true).removeClass("submit").addClass("submit_disabled");
		}
	});
    $(".add-note form").on({
        mouseover:function(){
            $(this).find(".arr").addClass("focus");
        },
        mouseleave:function(){
            $(this).find(".arr").removeClass("focus");
        },
        focus:function(){
            $(this).find(".arr").addClass("focus");
        },
        blur:function(){
            $(this).find(".arr").removeClass("focus");
        }
    });
    $(".load-entity input[type='submit']").on("click",function(){
        var entity_url = $("input[name='cand_url']").val();
        var request_url = $(".load-entity").attr("sd");
        var thisObj = $(this);
        $.ajax({
            type:"post",
            url:request_url,
            data:{cand_url:entity_url},
            dataType:"json",
            success:function(data){
                console.log(data);
                if(data.status == "EXIST"){
                    $(".entity_already_exist a").attr("href","/detail/"+data.data.entity_hash);
                    $(".entity_already_exist").show();
                }else{
                    $(".entity_already_exist").hide();
                    $(".entity-detail").slideDown();
                    $(".add-note").show();
                    $(".detail_title span:eq(1)").text(data.data.taobao_title);
                    $(".detail_title_input").val(data.data.taobao_title);
                    $(".detail_chief_url img").attr("src",data.data.chief_image_url);
                    $(".add-note .user_avatar").attr("src",data.data.user_context.avatar_small);
                    $(".detail_thumb_images").html("");
                    thisObj.val("重新载入");
                    thisObj.css({
                        background:"#bbb",
                        border:"1px solid #ddd",
                        color:"white",
                        outline:"none"
                    });
                    for(var i=0;i<data.data.thumb_images.length;i++){
                        if(i==0){
                            $(".detail_thumb_images").append('<div><img class="current_img" src='+data.data.thumb_images[i]+'_50x50.jpg'+'></div>');
                        }else{
                            $(".detail_thumb_images").append('<div><img src='+data.data.thumb_images[i]+'_50x50.jpg'+'></div>');
                        }
                        $('<input name="thumb_images" type="hidden" value='+data.data.thumb_images[i]+'>').appendTo($(".detail form"));
                    }

                    $('<input type="hidden" name="shop_link" value="'+data.data.shop_link+'"><input type="hidden" name="taobao_id" value="'+data.data.taobao_id+'"><input type="hidden" name="shop_nick" value="'+data.data.shop_nick+'"><input type="hidden" name="url" value="'+data.data.cand_url+'"><input type="hidden" name="price" value="'+data.data.price+'"><input type="hidden" name="chief_image_url" value="'+data.data.chief_image_url+'"><input type="hidden" name="cid" value="'+data.data.cid+'"><input type="hidden" name="taobao_title" value="'+data.data.taobao_title+'"><input type="hidden" name="selected_category_id" value="'+data.data.selected_category_id+'"><input name="user_id" type="hidden" value="'+data.data.user_context.user_id+'">').appendTo($(".detail form"));
                }
            },
            error:function(msg){
                console.log(msg);
            }
        });
    });
    $(".detail_taobao_brand").on("input propertychange",function(){
        var brand = $(this).val();
        if(brand.length>0){
            $(".detail_title span:eq(0)").text(brand+" --- ");
        }else{
            $(".detail_title span:eq(0)").text(brand);
        }
    });
    $(".detail_title_input").on("input propertychange",function(){
        var title = $(this).val();
        $(".detail_title span:eq(1)").text(title);
    });
    
    $("#add-entity .detail-img div img").live("click",function(){
        $(".current_img").removeClass("current_img");
        $(this).addClass("current_img");
        var img_url = $(this).attr("src");
        var big_url = img_url.replace('50x50','300x300');
        $(".detail_chief_url img").attr("src",big_url);
    });
    $(".detail form").on("submit",function(){
        var brand = $(".detail_taobao_brand").val();
        var taobao_title = $(".detail_title_input").val();
        $('<input type="hidden" name="brand" value="'+brand+'">').appendTo($(".detail form"));
        $('<input type="hidden" name="title" value="'+taobao_title+'">').appendTo($(".detail form"));
        return true;
    });
    $("#forget_sendmail").on("click",function(){
        var email = $(".forget_input").val();
        var request_url = $(".password").attr("sd");
        $.ajax({
            type:"post",
            url:request_url,
            data:{email:email},
            success:function(data){
                console.log(data);
                switch(data){
                    case "success":
                        send_status(false);
                        var s = 60;
                        $("#forget_sendmail").html("发送成功！<i>60</i>秒后可重新发送！").attr("send-status",1);
                        var t = setInterval(function(){
                            console.log(s);
                            s -=1;
                            if(s>=0)
                                $("#forget_sendmail").html("发送成功！<i>"+s+"</i>秒后可重新发送！");
                            else{
                                $("#forget_sendmail").html("发送邮件！").attr("send-status",0);
                                send_status(true);
                                clearInterval(t);
                            }
                        },1000);
                    break;
                    case "not_exist":
                        $(".forget_input_tip").html('该邮箱尚未注册，<a href="/register/">点此注册</a>').show();
                    break;
                    case "failed":
                        $(".forget_input_tip").html('发送失败,请尝试重新发送！').show();
                    break;
                    default:
                        $(".forget_input_tip").html('发送失败,请尝试重新发送！').show();
                    break;
                }
            }
        });
    });
    $(".forget_input").on("keyup change click",function(){
        if($("#forget_sendmail").attr("send-status") == 1){
            return false;
        }
        if($.trim($(this).val()).length>0)
        send_status(true);
        else
        send_status(false);
    });
    function send_status(flag){
        if(flag){
            $("#forget_sendmail").removeClass("btn-disabled").addClass("btn-update").removeAttr("disabled");
        }else{
            $("#forget_sendmail").removeClass("btn-update").addClass("btn-disabled").attr("disabled","true");
        }
    }

//    if ($.browser.msie) {
//        $('[placeholder]').focus(function() {
//            var input = $(this);
//            if (input.val() == input.attr('placeholder')) {
//                input.val('');
//                input.removeClass('placeholder');
//            }
//            }).blur(function() {
//                var input = $(this);
//                if (input.val() == '' || input.val() == input.attr('placeholder')) {
//                input.addClass('placeholder');
//                input.val(input.attr('placeholder'));
//            }
//            }).blur().parents('form').submit(function() {
//                $(this).find('[placeholder]').each(function() {
//                var input = $(this);
//                if (input.val() == input.attr('placeholder')) {
//                input.val('');
//            }
//        })
//    });
//    }
});
	
