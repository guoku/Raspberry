/**
 * Created by edison on 14-9-21.
 */

;(function ($, document, window) {


    var util = {
        like: function () {
            // 喜爱 like entity
//            var self = this;
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
//                console.log(url);
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
//                console.log($counter.text());
//                if (!self.isUserLogined()) {
//                    self.popLoginBox();
//                } else {
//                    var $like = $(this);
//                    var $counter = $like.find('.count');
//                    var url = $(this).attr("href");
//                    if(url[url.length-2] == 1)
//                    	var like_status = 0;
//                    else
//                    	var like_status = 1;
//                   	var s = url.replace(/\/[01]\//,"/"+like_status+"/");
//                   	$(this).attr("href",s);
//                    $.post(url, function (data) {
//                        var count = parseInt($counter.text());
//                        var result = parseInt(data);
//
//                        if (result === 1) {
//                            $counter.text(" "+(count + 1));
//                            $like.addClass('liked');
//                        } else if (result === 0) {
//                            $counter.text(" "+(count - 1));
//                            $like.removeClass('liked');
//                        }
//                    });
//                }

                e.preventDefault();
            });
        }
    };

    (function init() {

        util.like();

    })();


})(jQuery, document, window);