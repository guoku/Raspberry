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
    var $commentText = $form.find('input[name="comment_text"]');

    var replyToUser = '';
    var replyToComment = '';

    $this.find('.add-comment').on('click', function () {
      $noteComment.slideToggle('fast');

      $form.find('.cancel-comment').one('click', function () {
        $noteComment.slideUp('fast');

        replyToUser = '';
        replyToComment = '';
        $commentText.val('');
      });
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


  var Location = {
    location: ['安徽', '澳门', '北京', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '黑龙江', '湖北', '湖南',
      '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏', '青海', '山东', '山西', '陕西', '上海', '四川', '台湾', '天津', '西藏',
      '香港', '新疆', '云南', '浙江', '重庆', '海外'],
    city: [
      ['合肥', '安庆', '蚌埠', '亳州', '巢湖', '池州', '滁州', '阜阳', '淮北', '淮南', '黄山', '六安', '马鞍山', '宿州', '铜陵', '芜湖', '宣城'],
      ['澳门'],
      ['昌平', '朝阳', '崇文', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟', '密云', '平谷', '石景山', '顺义', '通州', '西城', '宣武', '延庆'],
      ['福州', '龙岩', '南平', '宁德', '莆田', '泉州', '三明', '厦门', '漳州'],
      ['兰州', '白银', '定西', '甘南', '嘉峪关', '金昌', '酒泉', '临夏', '陇南', '平凉', '庆阳', '天水', '武威', '张掖'],
      ['广州', '潮州', '东莞', '佛山', '河源', '惠州', '江门', '揭阳', '茂名', '梅州', '清远', '汕头', '汕尾', '韶关', '深圳', '阳江', '云浮', '湛江', '肇庆', '中山', '珠海'],
      ['桂林', '百色', '北海', '崇左', '防城港', '贵港', '河池', '贺州', '来宾', '柳州', '南宁', '钦州', '梧州', '玉林'],
      ['贵阳', '安顺', '毕节', '六盘水', '黔东南', '黔南', '黔西南', '铜仁', '遵义'],
      ['海口', '白沙', '保亭', '昌江', '澄迈', '儋州', '定安', '东方', '乐东', '临高', '陵水', '南沙群岛', '琼海', '琼中', '三亚', '屯昌', '万宁', '文昌', '五指山', '西沙群岛', '中沙群岛'],
      ['石家庄', '保定', '沧州', '承德', '邯郸', '衡水', '廊坊', '秦皇岛', '唐山', '邢台', '张家口'],
      ['郑州', '安阳', '鹤壁', '焦作', '开封', '洛阳', '漯河', '南阳', '平顶山', '濮阳', '三门峡', '商丘', '新乡', '信阳', '许昌', '周口', '驻马店'],
      ['哈尔滨', '大庆', '大兴安岭', '鹤岗', '黑河', '鸡西', '佳木斯', '牡丹江', '七台河', '齐齐哈尔', '双鸭山', '绥化', '伊春'],
      ['武汉', '鄂州', '恩施', '黄冈', '黄石', '荆门', '荆州', '潜江', '神农架', '十堰', '随州', '天门', '仙桃', '咸宁', '襄樊', '孝感', '宜昌'],
      ['长沙', '常德', '郴州', '衡阳', '怀化', '娄底', '邵阳', '湘潭', '湘西', '益阳', '永州', '岳阳', '张家界', '株洲'],
      ['长春', '白城', '白山', '吉林', '辽源', '四平', '松原', '通化', '延边'],
      ['南京', '常州', '淮安', '连云港', '南通', '苏州', '宿迁', '泰州', '无锡', '徐州', '盐城', '扬州', '镇江'],
      ['南昌', '抚州', '赣州', '吉安', '景德镇', '九江', '萍乡', '上饶', '新余', '宜春', '鹰潭'],
      ['沈阳', '鞍山', '本溪', '朝阳', '大连', '丹东', '抚顺', '阜新', '葫芦岛', '锦州', '辽阳', '盘锦', '铁岭', '营口'],
      ['呼和浩特', '阿拉善', '巴彦淖尔', '包头', '赤峰', '鄂尔多斯', '呼伦贝尔', '通辽', '乌海', '乌兰察布', '锡林郭勒', '兴安'],
      ['银川', '固原', '石嘴山', '吴忠', '中卫'],
      ['西宁', '果洛', '海北', '海东', '海南', '海西', '黄南', '玉树'],
      ['济南', '滨州', '德州', '东营', '菏泽', '济宁', '莱芜', '聊城', '临沂', '青岛', '日照', '泰安', '威海', '潍坊', '烟台', '枣庄', '淄博'],
      ['太原', '长治', '大同', '晋城', '晋中', '临汾', '吕梁', '朔州', '忻州', '阳泉', '运城'],
      ['西安', '安康', '宝鸡', '汉中', '商洛', '铜川', '渭南', '咸阳', '延安', '榆林'],
      ['宝山', '长宁', '崇明', '奉贤', '虹口', '黄浦', '嘉定', '金山', '静安', '卢湾', '闵行', '南汇', '浦东', '普陀', '青浦', '松江', '徐汇', '杨浦', '闸北'],
      ['成都', '阿坝', '巴中', '达州', '德阳', '甘孜', '广安', '广元', '乐山', '凉山', '泸州', '眉山', '绵阳', '内江', '南充', '攀枝花', '遂宁', '雅安', '宜宾', '资阳', '自贡'],
      ['台北', '阿莲', '安定', '安平', '八德', '八里', '白河', '白沙', '板桥', '褒忠', '宝山', '卑南', '北斗', '北港', '北门', '北埔', '北投', '补子', '布袋', '草屯', '长宾', '长治', '潮州', '车城', '成功', '城中区', '池上', '春日', '刺桐', '高雄', '花莲', '基隆', '嘉义', '苗栗', '南投', '屏东', '台东', '台南', '台中', '桃园', '新竹', '宜兰', '彰化'],
      ['宝坻', '北辰', '大港', '东丽', '汉沽', '和平', '河北', '河东', '河西', '红桥', '蓟县', '津南', '静海', '南开', '宁河', '塘沽', '武清', '西青'],
      ['拉萨', '阿里', '昌都', '林芝', '那曲', '日喀则', '山南'],
      ['北区', '大埔区', '东区', '观塘区', '黄大仙区', '九龙', '葵青区', '离岛区', '南区', '荃湾区', '沙田区', '深水埗区', '屯门区', '湾仔区', '西贡区', '香港', '新界', '油尖旺区', '元朗区', '中西区'],
      ['乌鲁木齐', '阿克苏', '阿拉尔', '阿勒泰', '巴音郭楞', '博尔塔拉', '昌吉', '哈密', '和田', '喀什', '克拉玛依', '克孜勒苏柯尔克孜', '石河子', '塔城', '图木舒克', '吐鲁番', '五家渠', '伊犁'],
      ['昆明', '保山', '楚雄', '大理', '德宏', '迪庆', '红河', '丽江', '临沧', '怒江', '曲靖', '思茅', '文山', '西双版纳', '玉溪', '昭通'],
      ['杭州', '湖州', '嘉兴', '金华', '丽水', '宁波', '衢州', '绍兴', '台州', '温州', '舟山'],
      ['巴南', '北碚', '璧山', '长寿', '城口', '大渡口', '大足', '垫江', '丰都', '奉节', '涪陵', '合川', '江北', '江津', '九龙坡', '开县', '梁平', '南岸', '南川', '彭水', '綦江', '黔江', '荣昌', '沙坪坝', '石柱', '双桥', '铜梁', '潼南', '万盛', '万州', '巫山', '巫溪', '武隆', '秀山', '永川', '酉阳', '渝北', '渝中', '云阳', '忠县'],
      ['阿根廷', '埃及', '爱尔兰', '奥地利', '奥克兰', '澳大利亚', '巴基斯坦', '巴西', '保加利亚', '比利时', '冰岛', '朝鲜', '丹麦', '德国', '俄罗斯', '法国', '菲律宾', '芬兰', '哥伦比亚', '韩国', '荷兰', '加拿大', '柬埔寨', '喀麦隆', '老挝', '卢森堡', '罗马尼亚', '马达加斯加', '马来西亚', '毛里求斯', '美国', '秘鲁', '缅甸', '墨西哥', '南非', '尼泊尔', '挪威', '葡萄牙', '其它地区', '日本', '瑞典', '瑞士', '斯里兰卡', '泰国', '土耳其', '委内瑞拉', '文莱', '乌克兰', '西班牙', '希腊', '新加坡', '新西兰', '匈牙利', '以色列', '意大利', '印度', '印度尼西亚', '英国', '越南', '智利']
    ]
  };

  (function setAddress() {
    var $setting = $('#setting');
    var $location = $setting.find('.location');
    var $city = $setting.find('.city');
    var l = Location.location;
    var c = Location.city;

    var currP = $location.attr('data-p');
    var currC = $city.attr('data-c');
    var selectedP = 2;

    for (var i = 0; i < l.length; i++) {
      var $option = $('<option>').val(l[i])
        .text(l[i])
        .appendTo($location);

      if (currP === l[i]) {
        $option[0].selected = true;
        selectedP = i;
      }
    }

    var cities = c[selectedP];

    for (var i = 0; i < cities.length; i++) {
      var $option = $('<option>').val(cities[i])
        .text(cities[i])
        .appendTo($city);

      if (currC === cities[i]) {
        $option[0].selected = true;
      }
    }

    $location.change(function () {
      var currP = $(this).val();
      var selectedP = l.indexOf(currP);
      var cities = c[selectedP];
      $city.html('');

      for (var i = 0; i < cities.length; i++) {
        $('<option>').val(cities[i])
        .text(cities[i])
        .appendTo($city);
      }
    });
  })();


})(jQuery, document, window);