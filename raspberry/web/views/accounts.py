# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import json

from base.user import User
from util import get_request_user_context


MAX_SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 14  # two weeks


def _validate_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def _check_nickname_valid(nickname):
    _result = None
    if nickname is None or len(nickname) == 0:
        _result = '昵称不能为空'
    elif User.nickname_exist(nickname):
        _result = '昵称已经被占用'
    return _result


def _check_email_valid(email):
    _result = None
    if email is None or len(email) == 0:
        _result = '邮箱号不能为空'
    elif not _validate_email(email):
        _result = '邮箱号不正确'
    return _result


def _check_password_valid(password):
    _result = None
    if password is None or len(password) == 0:
        _result = '密码不能为空'
    elif len(password) < 6:
        _result = '密码必须大于6位'
    return _result


def is_nickname_used(nickname):
    _success = not User.nickname_exist(nickname)
    return HttpResponse(json.dumps(_success))


def is_email_used(email):
    _success = not User.email_exist(email)
    return HttpResponse(json.dumps(_success))


def register(request, template='accounts/register.html'):
    if request.method == 'GET':
        return render_to_response(
            template,
            {

            },
            context_instance=RequestContext(request)
        )

    else:
        _nickname = request.POST.get('nickname', None)
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)

        _error = {
            'nickname' : _check_nickname_valid(_nickname),
            'email' : _check_email_valid(_email),
            'psw' : _check_password_valid(_password)
        }

        if _error['email'] is None and User.email_exist(_email):
            _error['email'] = '邮箱已经被注册'

        if _error['nickname'] is None and _error['email'] is None and _error['psw'] is None:
            _new_user = User.create(_email, _password)
            _new_user.set_profile(_nickname)
            # TODO
            return HttpResponseRedirect('account/login/')

        return render_to_response(
            template,
            {
                'error': _error
            },
            context_instance=RequestContext(request)
        )


def login(request, template='accounts/login.html'):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if request.method == 'GET':
        _next = request.GET.get('next', None)

        return render_to_response(
            template,
            {
                'next' : _next
            },
            context_instance=RequestContext(request)
        )

    else:
        _next = request.POST.get('next', None)
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _remember_me = request.POST.get("remember_me", None)

        _error = {
            'email' : _check_email_valid(_email),
            'psw' : _check_password_valid(_password)
        }

        if _error['email'] is None and _error['psw'] is None:
            _user_id = User.get_user_id_by_email(_email)

            if _user_id is None:
                _error['email'] = '邮箱未注册'

            else:
                _username = User(_user_id).get_username()
                _user = authenticate(username=_username, password=_password)

                if _user is None:
                    _error['psw'] = '密码不正确'

                elif not _user.is_active:
                    _error['email'] = '帐号已冻结'

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
                'error' : _error
            },
            context_instance=RequestContext(request)
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
def check_curr_psw(request):
    if request.method == 'POST':
        _user = User(request.user.id)
        _psw = request.POST.get('psw', None)

        if _psw is not None:
            return _user.check_auth(_psw)


@login_required
def setting(request, template='accounts/setting.html'):
    _user = User(request.user.id)
    _user_context = _user.read()

    if request.method == 'GET':
        return render_to_response(
            template,
            {
                'user_context': _user_context,
            },
            context_instance=RequestContext(request)
        )

    else:
        _curr_psw = request.POST.get('current_psw', None)
        _error = {}

        if _curr_psw is not None:
            # set password
            _new_psw = request.POST.get('new_psw', None)
            _confirm_psw = request.POST.get('confirm_psw', None)

            if len(_curr_psw) < 6 or not _user.check_auth(_curr_psw):
                _error['psw'] = '当前密码不正确'

            elif len(_new_psw) < 6 or len(_confirm_psw) < 6:
                _error['psw'] = '秘密不能少于6位'

            elif _new_psw != _confirm_psw:
                _error['psw'] = '两次密码不一致'

            else:
                _user.reset_account(password=_new_psw)

        else:
            # set basic info
            _nickname = request.POST.get('nickname', None)
            _email = request.POST.get('email', None)
            _bio = request.POST.get('bio', None)
            _location = request.POST.get('location', None)
            _city = request.POST.get('city', None)
            _gender = request.POST.get('gender', None)
            _website = request.POST.get('website', None)

            _len = len(_nickname)
            if _len == 0 or _len > 15:
                _nickname = None

            _len = len(_bio)
            if _len == 0:
                _bio = None

            _len = len(_website)
            if _len == 0:
                _website = None

            _user.set_profile(_nickname, location=_location, city=_city, gender=_gender, bio=_bio, website=_website)

            if _validate_email(_email):
                _user.reset_account(email=_email)

        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def upload_avatar(request):
    pass


@login_required
def update_avatar(request):
    pass