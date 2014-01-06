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
    if request.method == 'GET':
        _nickname = request.GET.get('nickname', None)
        _ret = not User.nickname_exist(_nickname)

        return HttpResponse(int(_ret))


def check_email_available(request):
    if request.method == 'GET':
        _email = request.GET.get('email', None)
        _ret = not User.email_exist(_email)

        return HttpResponse(int(_ret))


def register(request, template='accounts/register.html'):
    if request.method == 'GET':
        return render_to_response(
            template,
            {},
            context_instance=RequestContext(request)
        )

    else:
        _nickname = request.POST.get('nickname', None)
        _email = request.POST.get('email', None)
        _psw = request.POST.get('psw', None)
        _error = {}

        _error['nickname'] = v_check_nickname(_nickname)

        if _error['nickname'] is None:
            if User.nickname_exist(_nickname):
                _error['nickname'] = '昵称已经被占用'

            else:
                _error['email'] = v_check_email(_email)

                if _error['email'] is None:
                    if User.email_exist(_email):
                        _error['email'] = '邮箱已经被注册'

                    else:
                        _error['psw'] = v_check_psw(_psw)

                        if _error['psw'] is None:
                            _new_user = User.create(_email, _psw)
                            _new_user.set_profile(_nickname)

                            _username = _new_user.get_username()
                            _new_user = authenticate(username=_username, password=_psw)
                            auth_login(request, _new_user)

                            return HttpResponseRedirect('/accounts/setting/')

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
        _psw = request.POST.get('psw', None)
        _remember_me = request.POST.get("remember_me", None)
        _error = {}

        _error['email'] = v_check_email(_email)

        if _error['email'] is None:
            _user_id = User.get_user_id_by_email(_email)

            if _user_id is None:
                _error['email'] = '邮箱未注册'

            else:
                _error['psw'] = v_check_psw(_psw)

                if _error['psw'] is None:
                    _username = User(_user_id).get_username()
                    _user = authenticate(username=_username, password=_psw)

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
    if request.method == 'GET':
        _user_context = User(request.user.id).read()

        return render_to_response(
            template,
            {
                'user_context' : _user_context,
            },
            context_instance=RequestContext(request)
        )


@login_required
def set_base(request, template='accounts/setting.html'):
    if request.method == 'POST':
        _user = User(request.user.id)
        _user_context = _user.read()
        _error = {}

        _nickname = request.POST.get('nickname', None)
        _email = request.POST.get('email', None)
        _bio = request.POST.get('bio', None)
        _location = request.POST.get('location', None)
        _city = request.POST.get('city', None)
        _gender = request.POST.get('gender', None)
        _website = request.POST.get('website', None)

        _error['nickname'] = v_check_nickname(_nickname)

        if _error['nickname'] is None:
            _error['email'] = v_check_email(_email)

            if _error['email'] is None:
                _error['bio'] = v_check_bio(_bio)

                if _error['bio'] is None:
                    _error['website'] = v_check_website(_website)

                    if _error['website'] is None:
                        # 验证性别和地理位置是否合法 不合法则用原值
                        if not v_validate_gender(_gender):
                            _gender = _user_context['gender']

                        if not v_validate_location(_location, _city):
                            _location = _user_context['location']
                            _city = _user_context['city']

                        _user.set_profile(_nickname, location=_location, city=_city, gender=_gender, bio=_bio, website=_website)
                        _user.reset_account(email=_email)

        return render_to_response(
            template,
            {
                'user_context' : _user_context,
                'error' : _error
            },
            context_instance=RequestContext(request)
        )


@login_required
def set_psw(request, template='accounts/setting.html'):
    if request.method == 'POST':
        _user = User(request.user.id)
        _user_context = _user.read()
        _error = {}

        _curr_psw = request.POST.get('current_psw', None)
        _new_psw = request.POST.get('new_psw', None)
        _confirm_psw = request.POST.get('confirm_psw', None)

        if _curr_psw is not None or len(_curr_psw) < 6 or not _user.check_auth(_curr_psw):
            _error['psw'] = '当前密码不正确'

        elif len(_new_psw) < 6 or len(_confirm_psw) < 6:
            _error['psw'] = '秘密不能少于6位'

        elif _new_psw != _confirm_psw:
            _error['psw'] = '两次密码不一致'

        else:
            _user.reset_account(password=_new_psw)

        return render_to_response(
            template,
            {
                'user_context' : _user_context,
                'error' : _error
            },
            context_instance=RequestContext(request)
        )


@login_required
def upload_avatar(request):
    pass


@login_required
def update_avatar(request):
    pass