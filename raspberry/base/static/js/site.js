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

    var detail = {

        detailImageHover: function () {
            // 鼠标放细节图上后效果

            $('#detail').each(function () {
                var $this = $(this);
                $this.find('.detail-img img').on('mouseover', function () {
//                    console.log(this);
                    var re = /64x64/;
                    var url_string = this.src.replace(re, '640x640');
                    $this.find('.entity-chief-img img')[0].src = url_string;
                });
            });
        }
    };

    (function init() {

        util.like();

        detail.detailImageHover();

    })();


})(jQuery, document, window);