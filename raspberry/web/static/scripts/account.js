;(function ($) {
  var V = {};

  V.checkNickname = function ($nickname, valid, remote) {
    var nickname = $.trim($nickname.val());
    var result;

    if (nickname.length === 0) {
      result = '昵称不能为空';
    } else if (nickname.length > 15) {
      result = '昵称不能超过15个字';
    } else if (remote) {
      var url = '/accounts/register/check_nickname_available/';
      $.get(url, { nickname: nickname }, function (data) {
        var result = parseInt(data);
        valid['nickname'] = !!result;

        if (result === 0) {
          valid['nickname'] = false;
          showErrMsg($nickname, '昵称已经被占用');
        }
      });
    }

    valid['nickname'] = !result;
    showErrMsg($nickname, result);
  };

  V.checkEmail = function ($email,  valid, remote) {
    var email = $.trim($email.val());
    var result;

    if (email.length === 0) {
      result = '请填写邮箱';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      result = '请输入正确的邮箱地址';
    } else if (remote) {
      var url = '/accounts/register/check_email_available/';
      $.get(url, { email: email }, function (data) {
        var result = parseInt(data);
        valid['nickname'] = !!result;

        if (result === 0) {
          showErrMsg($email, '邮箱已经被注册');
        }
      });
    }

    valid['email'] = !result;
    showErrMsg($email, result);
  };

  V.checkPsw = function ($psw, valid) {
    var psw = $.trim($psw.val());
    var result;

    if (psw.length < 6) {
      result = '密码至少6位';
    } else if (psw.length > 20) {
      result = '密码最多20位';
    }

    valid['psw'] = !result;
    showErrMsg($psw, result);
  };


  function showErrMsg($formEle, msg) {
    var $errorEle = $formEle.next('.error-info');

    if (!msg) {
      $errorEle.remove();
    } else if ($errorEle[0]) {
      $errorEle.text(msg);
    } else {
      $formEle.after('<span class="error-info">' + msg + '</span>');
    }
  }

  // 注册
  var $rForm = $('form#register');
  var $rNickName = $rForm.find('#nickname');
  var $rEmail = $rForm.find('#email');
  var $rPsw = $rForm.find('#psw');
  var rValid = {};

  $rNickName.on('change', function () {
    V.checkNickname($(this), rValid, true);
  });

  $rEmail.on('change', function () {
    V.checkEmail($(this), rValid, true);
  });

  $rPsw.on('change', function () {
    V.checkPsw($(this), rValid);
  });

  $rForm.on('submit', function (e) {
    if (rValid.nickname && rValid.email && rValid.psw) {
      return;
    }

    V.checkNickname($rNickName, rValid, true);
    V.checkEmail($rEmail, rValid, true);
    V.checkPsw($rPsw, rValid);

    e.preventDefault()
  });

  // 登录
  var $lForm = $('form#login');
  var $lEmail = $lForm.find('#email');
  var $lPsw = $lForm.find('#psw');
  var lValid = {};

  $lEmail.on('change', function () {
    V.checkEmail($(this), lValid);
  });

  $lPsw.on('change', function () {
    V.checkPsw($(this), lValid);
  });

  $lForm.on('submit', function (e) {
    if (lValid.email && lValid.psw) {
      return;
    }

    V.checkEmail($lEmail, lValid);
    V.checkPsw($lPsw, lValid);

    e.preventDefault()
  });


})(jQuery);
