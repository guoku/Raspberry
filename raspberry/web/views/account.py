# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json

from base.user import User
from validation import *


MAX_SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 14  # two weeks


def check_nickname_available(request):
    """注册时 Ajax 方式验证 nickname 是否可用"""

    if request.method == 'GET':
        _nickname = request.GET.get('nickname', None)
        _ret = not User.nickname_exist(_nickname)

        return HttpResponse(int(_ret))


def check_email_available(request):
    """注册时 Ajax 方式验证 email 是否可用"""

    if request.method == 'GET':
        _email = request.GET.get('email', None)
        _ret = not User.email_exist(_email)

        return HttpResponse(int(_ret))


def register(request, template = 'account/register.html'):
    if request.method == 'GET':
        return render_to_response(
            template,
            {},
            context_instance = RequestContext(request)
        )

    else:
        _nickname = request.POST.get('nickname', None)
        _email = request.POST.get('email', None)
        _psw = request.POST.get('psw', None)
        _error = {}

        _error['nickname'] = v_check_nickname(_nickname, must_not_exist = True)

        if _error['nickname'] is None:
            _error['email'] = v_check_email(_email, must_not_exist = True)

            if _error['email'] is None:
                _error['psw'] = v_check_psw(_psw)

                if _error['psw'] is None:
                    _new_user = User.create(_email, _psw)
                    _new_user.set_profile(_nickname)

                    _username = _new_user.get_username()
                    _new_user = authenticate(username = _username, password = _psw)
                    auth_login(request, _new_user)

                    return HttpResponseRedirect('/register/bio/')

        return render_to_response(
            template,
            {
                'error' : _error
            },
            context_instance = RequestContext(request)
        )


@login_required
def register_bio(request, template = 'account/register_bio.html'):
    """ 注册成功后完善用户信息 """

    _user = User(request.user.id)
    _user_context = _user.read()

    if request.method == 'GET':
        return render_to_response(
            template,
            {
                'user_context' : _user_context
            },
            context_instance = RequestContext(request)
        )

    else:
        _bio = request.POST.get('bio', None)
        _location = request.POST.get('location', None)
        _city = request.POST.get('city', None)
        _gender = request.POST.get('gender', None)
        _website = request.POST.get('website', None)

        _error = v_check_bio(_bio)

        if _error is None:
            _error = v_check_website(_website)

            if _error is None:
                # 验证性别和地理位置是否合法 不合法则用原值
                if not v_validate_gender(_gender):
                    _gender = _user_context['gender']

                if not v_validate_location(_location, _city):
                    _location = _user_context['location']
                    _city = _user_context['city']

                try:
                    _nickname = _user_context['nickname']
                    _user.set_profile(_nickname, location = _location, city = _city, gender = _gender,
                                  bio = _bio, website = _website)
                    return HttpResponseRedirect('/selected/')

                except User.NicknameExistAlready:
                    _error = u'昵称已经被占用'

        return render_to_response(
            template,
            {
                'user_context': _user_context,
                'error': _error
            },
            context_instance = RequestContext(request)
        )


def login(request, template = 'account/login.html'):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if request.method == 'GET':
        _next = request.GET.get('next', None)

        return render_to_response(
            template,
            {
                'next' : _next
            },
            context_instance = RequestContext(request)
        )

    else:
        _next = request.POST.get('next', None)
        _email = request.POST.get('email', None)
        _psw = request.POST.get('psw', None)
        _remember_me = request.POST.get("remember_me", None)
        _error = {}

        _error['email'] = v_check_email(_email)

        if _error['email'] is None:
            _user_id = User.get_user_id_by_email(_email)

            if _user_id is None:
                _error['email'] = u'邮箱未注册'

            else:
                _error['psw'] = v_check_psw(_psw)

                if _error['psw'] is None:
                    _username = User(_user_id).get_username()
                    _user = authenticate(username = _username, password = _psw)

                    if _user is None:
                        _error['psw'] = u'密码不正确'

                    elif not _user.is_active:
                        _error['email'] = u'帐号已冻结'

                    else:
                        auth_login(request, _user)

                        if _remember_me is not None:
                            request.session.set_expiry(MAX_SESSION_EXPIRATION_TIME)

                        if _next is not None:
                            return HttpResponseRedirect(_next)

                        return HttpResponseRedirect('/selected/')

        return render_to_response(
            template,
            {
                'error' : _error,
                'email' : _email
            },
            context_instance = RequestContext(request)
        )


def login_by_sina(request):
    pass


def login_by_taobao(request):
    pass


@login_required
def logout(request):
    auth_logout(request)
    request.session.set_expiry(0)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def s_check_nickname_available(request):
    """用户设置时 Ajax 方式验证 nickname 是否可用"""

    if request.method == 'GET':
        _nickname = request.GET.get('nickname', None)
        _user_context = User(request.user.id).read()
        _ret = 1

        if User.nickname_exist(_nickname) and _user_context['nickname'] != _nickname:
            _ret = 0

        return HttpResponse(_ret)


@login_required
def s_check_email_available(request):
    """用户设置时 Ajax 方式验证 email 是否可用"""

    if request.method == 'GET':
        _email = request.GET.get('email', None)
        _user_context = User(request.user.id).read()
        _ret = 1

        if User.email_exist(_email) and _user_context['email'] != _email:
            _ret = 0

        return HttpResponse(_ret)


def _set_base(request, template):
    _user = User(request.user.id)
    _user_context = _user.read()
    _error = None
    _success = None

    _nickname = request.POST.get('nickname', None)
    _email = request.POST.get('email', None)
    _bio = request.POST.get('bio', None)
    _location = request.POST.get('location', None)
    _city = request.POST.get('city', None)
    _gender = request.POST.get('gender', None)
    _website = request.POST.get('website', None)

    _error = v_check_nickname(_nickname)

    if _error is None:
        _error = v_check_email(_email)

        if _error is None:
            _error = v_check_bio(_bio)

            if _error is None:
                _error = v_check_website(_website)

                if _error is None:
                    # 验证性别和地理位置是否合法 不合法则用原值
                    if not v_validate_gender(_gender):
                        _gender = _user_context['gender']

                    if not v_validate_location(_location, _city):
                        _location = _user_context['location']
                        _city = _user_context['city']

                    _success = '设置成功'

                    try:
                        _user.set_profile(_nickname, location = _location, city = _city, gender = _gender,
                                          bio = _bio, website = _website)
                    except User.NicknameExistAlready:
                        _error = u'昵称已经被占用'
                        _success = None

                    try:
                        _user.reset_account(email = _email)
                    except User.EmailExistAlready:
                        _error = u'邮箱已经被占用'
                        _success = None

                    # 读取最新信息
                    _user_context = User(request.user.id).read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'base_error' : _error,
            'base_success' : _success
        },
        context_instance = RequestContext(request)
    )


def _set_psw(request, template):
    _user = User(request.user.id)
    _user_context = _user.read()
    _error = None
    _success = None

    _curr_psw = request.POST.get('current_psw', None)
    _new_psw = request.POST.get('new_psw', None)
    _confirm_psw = request.POST.get('confirm_psw', None)

    if _curr_psw is None or len(_curr_psw) < 6 or not _user.check_auth(_curr_psw):
        _error = u'当前密码不正确'

    elif len(_new_psw) < 6 or len(_confirm_psw) < 6:
        _error = u'秘密不能少于6位'

    elif _new_psw != _confirm_psw:
        _error = u'两次密码不一致'

    else:
        _user.reset_account(password = _new_psw)
        _success = u'密码设置成功'

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'psw_error' : _error,
            'psw_success' : _success
        },
        context_instance = RequestContext(request)
    )


@login_required
def setting(request, template = 'account/setting.html'):
    if request.method == 'GET':
        _user_context = User(request.user.id).read()

        return render_to_response(
            template,
            {
                'user_context' : _user_context,
            },
            context_instance = RequestContext(request)
        )

    if request.method == 'POST':
        _type = request.POST.get('type', None)

        if _type is not None:
            _type = _type.strip()

            if _type == 'base':
                return _set_base(request, template)

            elif _type == 'psw':
                return _set_psw(request, template)


@login_required
def upload_avatar(request):
    pass


@login_required
def update_avatar(request):
    pass