;(function ($) {
  // 注册
  var $rForm = $('form#register');
  var $rNickName = $rForm.find('#nickname');
  var $rEmail = $rForm.find('#email');
  var $rPsw = $rForm.find('#psw');
  var rV = new V();

  $rNickName.on('change', function () {
    rV.checkNickname($(this), true);
  });

  $rEmail.on('change', function () {
    rV.checkEmail($(this), true);
  });

  $rPsw.on('change', function () {
    rV.checkPsw($(this));
  });

  $rForm.on('submit', function (e) {
    if (rV.isValid()) {
      return;
    }

    rV.checkNickname($rNickName, true);
    rV.checkEmail($rEmail, true);
    rV.checkPsw($rPsw);

    e.preventDefault()
  });

  // 登录
  var $lForm = $('form#login');
  var $lEmail = $lForm.find('#email');
  var $lPsw = $lForm.find('#psw');
  var lV = new V();

  $lEmail.on('change', function () {
    lV.checkEmail($(this));
  });

  $lPsw.on('change', function () {
    lV.checkPsw($(this));
  });

  $lForm.on('submit', function (e) {
    if (lV.isValid()) {
      return;
    }

    lV.checkEmail($lEmail);
    lV.checkPsw($lPsw);

    e.preventDefault()
  });


  // for validation
  function V() {
    this.valid = [];
  }

  V.prototype._showErrMsg = function ($formEle, msg) {
    var $errorEle = $formEle.next('.error-info');

    if (!msg) {
      $errorEle.remove();
    } else if ($errorEle[0]) {
      $errorEle.text(msg);
    } else {
      $formEle.after('<span class="error-info">' + msg + '</span>');
    }
  };

  V.prototype.checkNickname = function ($nickname, remote) {
    var nickname = $.trim($nickname.val());
    var result;
    var valid = this.valid;
    var showErrMsg = this._showErrMsg;

    if (nickname.length === 0) {
      result = '昵称不能为空';
    } else if (nickname.length > 15) {
      result = '昵称不能超过15个字';
    } else if (remote) {
      var url = '/accounts/register/check_nickname_available/';
      $.get(url, { nickname: nickname }, function (data) {
        var result = parseInt(data);
        valid.push(!!result);

        if (result === 0) {
          showErrMsg($nickname, '昵称已经被占用');
        }
      });
    }

    valid.push(!result);
    showErrMsg($nickname, result);
  };

  V.prototype.checkEmail = function ($email, remote) {
    var email = $.trim($email.val());
    var result;
    var valid = this.valid;
    var showErrMsg = this._showErrMsg;

    if (email.length === 0) {
      result = '请填写邮箱';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      result = '请输入正确的邮箱地址';
    } else if (remote) {
      var url = '/accounts/register/check_email_available/';
      $.get(url, { email: email }, function (data) {
        var result = parseInt(data);
        valid.push(!!result);

        if (result === 0) {
          showErrMsg($email, '邮箱已经被注册');
        }
      });
    }

    valid.push(!result);
    showErrMsg($email, result);
  };

  V.prototype.checkPsw = function ($psw) {
    var psw = $.trim($psw.val());
    var result;
    var valid = this.valid;
    var showErrMsg = this._showErrMsg;

    if (psw.length < 6) {
      result = '密码至少6位';
    } else if (psw.length > 20) {
      result = '密码最多20位';
    }

    valid.push(!result);
    showErrMsg($psw, result);
  };

  V.prototype.isValid = function () {
    var len = this.valid.length;
    if (len === 0) {
      return false;
    }

    var ret = true;
    for (var i = 0; i < len; i++) {
      ret = ret && this.valid[i];
    }
    return ret;
  };

})(jQuery);
