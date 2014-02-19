# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.conf import settings
from web import taobao_utils
from web import sina_utils
from web import web_utils
from utils import fetcher
import json
import time
import re
from base.taobao_shop import TaobaoShop
from base.user import User
from urlparse import urlparse
from web.forms.account import SignInAccountForm, SignUpAccountFrom, SettingAccountForm
from django.utils.log import getLogger

log = getLogger('django')
# from base.user import User
from validation import *


MAX_SESSION_EXPIRATION_TIME = getattr(settings, 'SESSION_COOKIE_AGE', 1209600) # two weeks

REGISTER_TEMPLATES = {
    'register' : 'account/register.html',
    'register-bio' : 'account/register_bio.html',
}

class RegisterWizard(SessionWizardView):
    def get_template_names(self):
        return [REGISTER_TEMPLATES[self.steps.current]]

    def render(self, form=None, **kwargs):
        if self.request.user.is_authenticated():
            next_url = self.request.META.get('HTTP_REFERER', reverse("web_selection"))
            return HttpResponseRedirect(next_url)
        return super(RegisterWizard, self).render(form, **kwargs)

    def signup(self, form_list):
        signup_form = form_list[0]
        bio_form = form_list[1]
        signup_data = signup_form.cleaned_data
        bio_data = bio_form.cleaned_data
        _user_inst = web_utils.signup(
            signup_data['email'], 
            signup_data['password'], 
            signup_data['nickname'],
            location = bio_data['location'],
            city = bio_data['city'],
            gender = bio_data['gender'],
            bio = bio_data['bio'],
            website = bio_data['website']
        )
        _user = _user_inst.authenticate_without_password()
        auth_login(self.request, _user)
        return _user_inst

    def done(self, form_list, **kwargs):
        self.signup(form_list)
        return HttpResponseRedirect(reverse("web_selection"))

class ThirdPartyRegisterWizard(RegisterWizard):
    def get_template_names(self):
        return [REGISTER_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(ThirdPartyRegisterWizard, self).get_context_data(form = form, **kwargs)
        if self.steps.current == 'register':
            token = self.request.GET.get("token", None)
            if not token:
                raise Http404
            context['third_party_data'] = web_utils.get_temporary_storage(token)
            context['source'] = self.request.GET.get("source", None)
        return context
                
    def done(self, form_list, **kwargs):
        token = self.request.GET.get('token', None)
        source = self.request.GET.get('source', None)
        if not token:
            raise Http404
        third_party_data = web_utils.get_temporary_storage(token)
        _user_inst = self.signup(form_list)
        if source == "sina":
            _user_inst.bind_sina(
                sina_id = third_party_data['sina_id'],
                screen_name = third_party_data['screen_name'],
                access_token = third_party_data['access_token'],
                expires_in = third_party_data['expires_in']
            )
        elif source == "taobao":
            _user_inst.bind_taobao(
                taobao_id = third_party_data['taobao_id'],
                screen_name = third_party_data['screen_name'],
                taobao_token = third_party_data['access_token'],
                expires_in = third_party_data['expires_in']
            )
        else:
            raise Http404
        return HttpResponseRedirect(reverse("web_selection"))

def login(request, template = 'account/login.html'):
    redirect_url = web_utils.get_login_redirect_url(request)
    print redirect_url
    if not redirect_url:
        redirect_url = reverse('web_selection')
    print redirect_url
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)

    if request.method == 'POST':
        _forms = SignInAccountForm(request.POST)
        if _forms.is_valid():
            _remember_me = request.POST.get('remember_me', None)
            _user = _forms.cleaned_data['user']
            auth_login(request, _user)
            if _remember_me:
                request.session.set_expiry(MAX_SESSION_EXPIRATION_TIME)
            return HttpResponseRedirect(redirect_url)
        else:
            return render_to_response(
                template,
                { 
                    'forms' : _forms, 
                },
                context_instance = RequestContext(request)
            )

    elif request.method == 'GET':
        _forms = SignInAccountForm(initial={'next': redirect_url})
        return render_to_response(
            template,
            { 
                'forms' : _forms, 
            },
            context_instance = RequestContext(request)
        )

@require_GET
def login_by_sina(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['auth_next_url'] = next_url 
    return HttpResponseRedirect(sina_utils.get_login_url())

@require_GET
def auth_by_sina(request):
    code = request.GET.get("code", None)
    if code:
        _sina_data = sina_utils.get_auth_data(code)
        next_url = request.session.get('auth_next_url', reverse("web_selection"))
        try:
            _user_inst = User.login_by_sina(
                _sina_data['sina_id'], 
                sina_token = _sina_data['access_token'],
                screen_name = _sina_data['screen_name'], 
                expires_in = _sina_data['expires_in']
            )
        except User.LoginSinaIdDoesNotExist, e:
            _user_inst = None
        except:
            return HttpResponseServerError()
        source = request.session.get('auth_source', None)
        if source:
            if source == "login":
                if _user_inst:
                    user = _user_inst.authenticate_without_password()
                    auth_login(request, user)
                    return HttpResponseRedirect(next_url)
                else:
                    token = web_utils.generate_random_storage_key("sina_login")
                    web_utils.create_temporary_storage(token, **_sina_data)
                    return HttpResponseRedirect(reverse("web_third_party_register") + "?source=sina&token=" + token)
            elif source == "bind":
                try:
                    _user_inst.bind_sina(
                        sina_id = third_party_data['sina_id'],
                        screen_name = third_party_data['screen_name'],
                        access_token = third_party_data['access_token'],
                        expires_in = third_party_data['expires_in']
                    )
                except:
                    pass
                return HttpResponseRedirect(next_url)
            else:
                pass
        else:
            pass

@require_GET
@login_required
def bind_sina(request):
    request.session['auth_source'] = "bind"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['auth_next_url'] = next_url
    return HttpResponseRedirect(sina_utils.get_login_url())

@require_GET
@login_required
def unbind_sina(request):
    _user_inst = User(request.user.id)
    _user_inst.unbind_sina()
    redirect_url = request.GET.get("next", reverse("web_selection"))
    return HttpResponseRedirect(redirect_url)

def login_by_taobao(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['auth_next_url'] = next_url 
    return HttpResponseRedirect(taobao_utils.get_login_url())

def auth_by_taobao(request):
    code = request.GET.get("code", None)
    if code:
        _taobao_data = taobao_utils.get_auth_data(code)
        next_url = request.session.get('auth_next_url', reverse("web_selection"))
        try:
            _user_inst = User.login_by_taobao(
                _taobao_data['taobao_id'],
                taobao_token = _taobao_data['access_token'],
                screen_name = _taobao_data['screen_name'],
                expires_in = _taobao_data['expires_in'])
        except User.LoginTaobaoIdDoesNotExist, e:
            print e
            _user_inst = None
        except:
            return HttpResponseServerError()
        source = request.session.get('auth_source', None)
        if source:
            if source == "login":
                if _user_inst:
                    user = _user_inst.authenticate_without_password()
                    auth_login(request, user)
                    return HttpResponseRedirect(next_url)
                else:
                    token = web_utils.generate_random_storage_key("taobao_login")
                    web_utils.create_temporary_storage(token, **_taobao_data)
                    return HttpResponseRedirect(reverse("web_third_party_register") + "?source=taobao&token=" + token)
            elif source == "bind":
                try:
                    _user_inst.bind_taobao(
                        taobao_id = third_party_data['taobao_id'],
                        screen_name = third_party_data['screen_name'],
                        taobao_token = third_party_data['access_token'],
                        expires_in = third_party_data['expires_in']
                    )
                except:
                    pass
                return HttpResponseRedirect(next_url)
            else:
                pass
        else:
            pass

@require_GET
@login_required
def bind_taobao(request):
    request.session['auth_source'] = "bind"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['auth_next_url'] = next_url
    return HttpResponseRedirect(sina_utils.get_login_url())
    
@require_GET
@login_required
def unbind_taobao(request):
    _user_inst = User(request.user.id)
    _user_inst.unbind_taobao()
    redirect_url = request.GET.get("next", reverse("web_selection"))
    return HttpResponseRedirect(redirect_url)

@login_required
def logout(request):
    auth_logout(request)
    request.session.set_expiry(0)
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    return HttpResponseRedirect(next_url)

def forget_passwd(request):
    return

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
                        _user.set_profile(
                            _nickname, 
                            location = _location, 
                            city = _city, 
                            gender = _gender,
                            bio = _bio, 
                            website = _website
                        )
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
    # if request.method == 'GET':
    #     _user_context = User(request.user.id).read()
    #
    #     return render_to_response(
    #         template,
    #         {
    #             'user_context' : _user_context,
    #         },
    #         context_instance = RequestContext(request)
    #     )

    if request.method == 'POST':
        _type = request.POST.get('type', None)
        # 根据表单字段 type 判断是设置基本信息还是密码 type 只能是 base 或 psw

        if _type is not None:
            _type = _type.strip()

            if _type == 'base':
                return _set_base(request, template)

            elif _type == 'psw':
                return _set_psw(request, template)
    else:
        _user_context = User(request.user.id).read()
        forms = SettingAccountForm(initial = _user_context, prefix="settings")
        sub_forms = None
        return render_to_response(
            template,
            {
                'user_context' : _user_context,
                'forms': forms,
                'sub_forms': sub_forms,
            },
            context_instance = RequestContext(request),
        )

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
        return render_to_response(
            "bind_taobao_shop.html",
            { 
                "request_user_context" : request_user_context 
            },
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
                if not TaobaoShop.nick_exist(nick):
                    shop_info = fetcher.fetch_shop(taobao_item_info['shop_link'])
                    TaobaoShop.create(
                        nick,
                        shop_info['shop_id'],
                        shop_info['title'],
                        shop_info['type'],
                        shop_info['seller_id'],
                        shop_info['pic']
                    ) 
                return HttpResponseRedirect(reverse('bind_taobao_shop'))
            else:
                message.info(request, "错误的商品地址，请输入淘宝商品地址")
                return HttpResponseRedirect(reverse('bind_taobao_shop'))
        else:
            return HttpResponseRedirect(reverse('bind_taobao_shop'))

