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

        _nickname_error = _check_nickname_valid(_nickname)
        _email_error = _check_email_valid(_email)
        _password_error = _check_password_valid(_password)

        if User.email_exist(_email):
            _email_error = '邮箱已经被注册'

        if not(_nickname_error or _email_error or _password_error):
            _new_user = User.create(_email, _password)
            _new_user.set_profile(_nickname)
            # TODO
            return HttpResponseRedirect('account/login/')

        else:
            return render_to_response(
                template,
                {
                    'nickname_error' : _nickname_error,
                    'email_error' : _email_error,
                    'password_error' : _password_error
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

        _email_error = _check_email_valid(_email)
        _password_error = _check_password_valid(_password)

        if not(_email_error or _password_error):
            _user_id = User.get_user_id_by_email(_email)

            if _user_id is not None:
                _username = User(_user_id).get_username()
                _user = authenticate(username=_username, password=_password)

                if _user is not None:
                    if _user.is_active:
                        auth_login(request, _user)

                        if _remember_me is not None:
                            request.session.set_expiry(MAX_SESSION_EXPIRATION_TIME)

                        if _next is not None:
                            return HttpResponseRedirect(_next)

                        return HttpResponseRedirect('/selected/')

                    else:
                        _email_error = '帐号已冻结'
                else:
                    _password_error = '密码不正确'
            else:
                _email_error = '邮箱未注册'

        return render_to_response(
            template,
            {
                'email_error' : _email_error,
                'password_error' : _password_error
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
def setting(request, template='accounts/setting.html'):
    _user_context = get_request_user_context(request.user)

    if request.method == 'GET':
        return render_to_response(
            template,
            {
                'user_context': _user_context,
            },
            context_instance=RequestContext(request)
        )

    else:
        pass


@login_required
def upload_avatar(request):
    pass


@login_required
def update_avatar(request):
    pass