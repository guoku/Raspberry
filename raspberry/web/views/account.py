# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
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
from lotto.lib.player import check_player 
import json
import time
import re
from base.taobao_shop import TaobaoShop
from base.user import User
from urlparse import urlparse
from share.tasks import RetrievePasswordTask 
from web.forms.account import SignInAccountForm, SignUpAccountFrom, SettingAccountForm, ChangePasswordForm
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
    if not redirect_url:
        redirect_url = reverse('web_selection')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)

    if request.method == 'POST':
        # log.info(request.POST)
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
                    if not _user_inst:
                        _user_inst = User(request.user.id)
                    else:
                        _user_context = _user_inst.read()
                        if _user_context['user_id'] != request.user.id:
                            return HttpResponse("this sina account has been binded by another user")
                            
                    _user_inst.bind_sina(
                        sina_id = _sina_data['sina_id'],
                        screen_name = _sina_data['screen_name'],
                        access_token = _sina_data['access_token'],
                        expires_in = _sina_data['expires_in']
                    )
                except:
                    pass
                return HttpResponseRedirect(next_url)
            elif source == "lotto":
                _mobile_session = request.session.get('mobile_session', None)
                _lotto_token = check_player(
                    sina_id = _sina_data['sina_id'],
                    screen_name = _sina_data['screen_name'],
                    access_token = _sina_data['access_token'],
                    expires_in = _sina_data['expires_in'],
                    mobile_session = _mobile_session
                )
                return HttpResponseRedirect(reverse('lotto_share_to_sina_weibo') + '?token=' + _lotto_token)

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
                    if not _user_inst:
                        _user_inst = User(request.user.id)
                    else:
                        _user_context = _user_inst.read()
                        if _user_context['user_id'] != request.user.id:
                            return HttpResponse("this taobao accout has been binded by another user")
                    #Todo: handle errors
                    _user_inst.bind_taobao(
                        taobao_id = _taobao_data['taobao_id'],
                        screen_name = _taobao_data['screen_name'],
                        taobao_token = _taobao_data['access_token'],
                        expires_in = _taobao_data['expires_in']
                    )
                except e:
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
    return HttpResponseRedirect(taobao_utils.get_login_url())
    
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

def forget_passwd(request, template='account/forget_password.html'):

    if request.method == 'GET':
        return render_to_response(
            template,
            {
            },
            context_instance = RequestContext(request),
        )
    else:
        try:
            _email = request.POST.get('email', None)
            _user_id = User.get_user_id_by_email(_email)
            if _user_id == None:
                return HttpResponse('not_exist')
            else:
                RetrievePasswordTask.delay(_user_id)
                return HttpResponse('success')
        except Exception, e:
            return HttpResponse('failed')
  
        

@require_POST
@login_required
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST)
    _user = User(request.user.id)
    if form.is_valid():
        _user.reset_account(password=form.cleaned_data['new_password'])
    return HttpResponseRedirect(reverse("web_setting"))

@require_POST
@login_required
def update_profile(request):
    form = SettingAccountForm(request.POST)
    _user = User(request.user.id)
    if form.is_valid():
        _user.set_profile(
            nickname = form.cleaned_data['nickname'],
            location = form.cleaned_data['location'],
            city = form.cleaned_data['city'],
            gender = form.cleaned_data['gender'],
            bio = form.cleaned_data['bio'],
            website = form.cleaned_data['website'],
        )
    return HttpResponseRedirect(reverse("web_setting"))

@require_GET
@login_required
def setting(request, template = 'account/setting.html'):
    _msg_code = request.GET.get('msg', None)
    _user_context = User(request.user.id).read()
    profile_form = SettingAccountForm(initial = _user_context)
    password_form = ChangePasswordForm(request.user)
    return render_to_response(
        template,
        {
            'msg_code' : _msg_code,
            'user_context' : _user_context,
            'profile_form': profile_form,
            'password_form': password_form,
        },
        context_instance = RequestContext(request),
    )

@login_required
def update_avatar(request):
    if request.method == 'POST':
        _avatar_img = request.FILES.get('avatar_img', None)
        if _avatar_img is None:
            return HttpResponseRedirect(reverse('web_setting') + '?msg=0') 

        elif len(_avatar_img) / (1024 ** 2) > 2:
            return HttpResponseRedirect(reverse('web_setting') + '?msg=1') 

        else:
            if hasattr(_avatar_img, 'chunks'):
                _image_data = ''.join(chunk for chunk in _avatar_img.chunks())
            else:
                _image_data = _avatar_img.read()
        
        _user = User(request.user.id)
        _user.upload_avatar(_image_data)
        
        return HttpResponseRedirect(reverse('web_setting')) 

def reset_password(request, template='account/reset_password.html'):
    if request.method == "GET":
        _token = request.GET.get("token", None)
        if _token:
            _result = User.check_one_time_token(_token, "reset_password")
            if _result['status'] == 'available': 
                return render_to_response(
                    template, 
                    {
                        'status' : _result['status'], 
                        'token' : _token,
                        'user_context' : User(_result['user_id']).read() 
                    },
                    context_instance = RequestContext(request)
                )
            else:
                return render_to_response(
                    template,
                    { 
                        'status' : _result['status'] 
                    },
                    context_instance=RequestContext(request)
                )
    elif request.method == "POST":
        _token = request.POST.get("token", None)
        _password = request.POST.get("password", None)
        _result = User.check_one_time_token(_token, "reset_password")
        if _result['status'] == 'available': 
            _user = User(_result['user_id'])
            _user.reset_account(password=_password)
            User.confirm_one_time_token(_token)
            return HttpResponseRedirect(reverse('web_selection'))
        
        else:
            return render_to_response(
                template,
                { 
                    'status' : _result['status'] 
                },
                context_instance=RequestContext(request)
            )

