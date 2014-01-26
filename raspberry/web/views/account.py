# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
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

                    return HttpResponseRedirect(reverse('web_register_bio'))

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
                    return HttpResponseRedirect(reverse('web_selection'))

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

                        return HttpResponseRedirect(reverse('web_selection'))

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
        # 根据表单字段 type 判断是设置基本信息还是密码 type 只能是 base 或 psw

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
    if request.method == 'POST':
        _avatar_img = request.FILES.get('avatar_img', None)
        _ret = {
            'status': 1
        }

        if _avatar_img is None:
            _ret = {
                'status': 0,
                'msg': '未上传图片'
            }

        elif len(_avatar_img) / (1024 ** 2) > 2:
            _ret = {
                'status': 0,
                'msg': '图片太大'
            }

        else:
            if hasattr(_avatar_img, 'chunks'):
                _image_data = ''.join(chunk for chunk in _avatar_img.chunks())
            else:
                _image_data = _avatar_img.read()

            # TODO

        return HttpResponse(json.dumps(_ret))

<<<<<<< HEAD
=======

@login_required
def bind_taobao(request):
    request.session['bind_taobao_next_url'] = request.GET.get('next', None)
    request.session['back_to_url'] = reverse('check_taobao_binding')
    return HttpResponseRedirect(taobao_utils.get_login_url())

def taobao_auth(request):
    return HttpResponseRedirect(taobao_utils.auth(request))

def bind_taobao_check(request):
    access_token = request.session['taobao_access_token']
    taobao_id = request.session['taobao_id']
    expires_in = int(time.time()) + int(request.session['taobao_expires_in'])

    taobao_user = taobao_utils.get_taobao_user_info(access_token)
    user_id = request.user.id
    user_inst = User(user_id)
    if taobao_user:
        try:
            user_inst.bind_taobao(taobao_id, taobao_user['nick'], access_token, expires_in)
            if request.session.get('bind_taobao_next_url', None):
                next_url = request.session['bind_taobao_next_url']
                try:
                    del request.session['bind_taobao_next_url']
                except KeyError:
                  return HttpResponseRedirect(request.META['HTTP_REFERER'])
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except User.TaobaoIdExistAlready, e:
            return HttpResponse("taobao id exsits")
        except User.UserBindTaobaoAlready, e:
            return HttpResponse("you have binded taobao")
        except Exception, e:
            print e
            return HttpResponse("unknow error")
    else:
        HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bind_taobao_shop(request):
    user_id = request.user.id
    user_inst = User(user_id)
    request_user_context = user_inst.read()
    if request.method == "GET":
        if request_user_context.get("taobao_screen_name"):
            if request_user_context['taobao_token_expires_in'] < time.time():
                request_user_context['taobao_token_expired'] = True
            else:
                request_user_context['taobao_token_expired'] = False
        messages.info(request, "test, test" + unicode(int(time.time())))
        return render_to_response("bind_taobao_shop.html",
                                 { "request_user_context" : request_user_context },
                                 context_instance=RequestContext(request)
                                 )
    elif request.method == "POST":
        if not request_user_context.get("taobao_nick"):
            messages.info(request, "尚未绑定淘宝帐号") 
            return HttpResponseRedirect(reverse('bind_taobao_shop'))
        item_url = request.POST.get('item_url', None)
        if not item_url:
            message.info(request, "请输入商品地址")
            return HttpResponseRedirect(reverse('bind_taobao_shop'))
      
        hostname = urlparse(item_url).hostname
        if re.search(r"\b(tmall|taobao)\.(com|hk)$", hostname) != None:
            taobao_id = web_utils.parse_taobao_id_from_url(item_url)
            taobao_item_info = fetcher.fetch_item(taobao_id)
            nick = taobao_item_info['nick']
            if request_user_context.get('taobao_nick') == nick:
                user_inst.create_seller_info(nick)
                if TaobaoShop.nick_exist(nick):
                    shop_info = fetcher.fetch_shop(taobao_item_info['shop_link'])
                    TaobaoShop.create(nick,
                                      shop_info['shop_id'],
                                      shop_info['title'],
                                      shop_info['type'],
                                      shop_info['seller_id'],
                                      shop_info['pic']) 
                return HttpResponseRedirect(reverse('bind_taobao_shop'))
            else:
                message.info(request, "错误的商品地址，请输入淘宝商品地址")
                return HttpResponseRedirect(reverse('bind_taobao_shop'))
        else:
            return HttpResponseRedirect(reverse('bind_taobao_shop'))

#def login(request, template="login.html"):
#    redirect_url = web_utils.get_login_redirect_url(request)
#    if request.user.is_authenticated():
#        return HttpResponseRedirect(redirect_url)
#    
#    if request.method == "GET":
#        return render_to_response(template,
#                                  { "remember_me" : True, "next" : web_utils.get_redirect_url(request)},
#                                    context_instance=RequestContext(request))
#
#    elif request.method == "POST":
#        email = request.POST.get('email', None)
#        password = request.POST.get('password', None)
#        remember_me = request.POST.get("remember_me", None)
#        try:
#            user_inst = User.login(email, password)
#        except User.LoginEmailDoesNotExist, e: 
#            return render_to_response(template,
#                                      {'email' : email,
#                                       'remember_me' : remember_me,
#                                       'error_msg' : web_text.LOGIN_WRONG_EMAIL
#                                      },
#                                      context_instance=RequestContext(request))
#        except User.LoginPasswordIncorrect, e:
#            return render_to_response(template,
#                                      {'email' : email,
#                                       'remember_me' : remember_me,
#                                       'error_msg' : web_utils.LOGIN_WRONG_PASSWORD
#                                      },
#                                      context_instance=RequestContext(request))
#        user_context = user_inst.read()
#        user = authenticate(username = user_context['username'], password = password)
#        if not user.is_active:
#            return render_to_response(template,
#                                      {'email' : email,
#                                       'remember_me' : remember_me,
#                                       'error_msg' : web_utils.LOGIN_USER_NOT_ACTIVE
#                                      },
#                                      context_instance=RequestContext(request))
#        auth_login(request, user)
#        if not remember_me:
#            request.session.set_expiry(0)
#        else:
#            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
#        print redirect_url
#        return HttpResponseRedirect(redirect_url)
>>>>>>> 6f8d585e38b3f2195756576ba76485eb3fb589cc
