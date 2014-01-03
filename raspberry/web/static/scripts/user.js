;(function ($) {
  function validate(options) {
    var email = options.email;
    var nickname = options.nickname;
    var password = options.password;
    var result = {};

    if (email.length === 0) {
      result['emailError'] = '邮箱不能为空';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      result['emailError'] = '邮箱号不正确';
    }

    if (password.length < 6) {
      result['passwordError'] = '密码至少6位'
    }

    if (typeof nickname !== 'undefined' && nickname.length === 0) {
      result['nicknameError'] = '昵称不能为空';
    }

    if (result.emailError || result.passwordError || result.nicknameError) {
      return result;
    }

    return null;
  }

  $('form').submit(function (e) {
    var $email = $("#email");
    var $password = $('#password');
    var $nickname = $('#nickname');

    var email = $.trim($email.val());
    var password = $.trim($password.val());
    var nickname = $nickname[0] && $.trim($nickname.val());

    var valid = validate({
      email: email,
      password: password,
      nickname: nickname
    });

    if (!valid) {
      return true;
    }

    addInfo($email, valid.emailError);
    addInfo($password, valid.passwordError);
    $nickname && addInfo($nickname, valid.nicknameError);

    function addInfo(node, text) {
      var errorNode = node.next('.error-info');
      if (!text) {
        errorNode.remove();
      } else if (errorNode[0]) {
        errorNode.text(text)
      } else {
        node.after('<span class="error-info">' + text + '</span>');
      }
    }

    e.preventDefault();
  });

})(jQuery);
