#coding=utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
from base.user import User
from base.taobao_shop import TaobaoShop
from web import taobao_utils
from web import web_utils
from web import web_text
from utils import fetcher
import re
import time

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

def login(request, template="login.html"):
    redirect_url = web_utils.get_login_redirect_url(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)
    
    if request.method == "GET":
        return render_to_response(template,
                                  { "remember_me" : True, "next" : web_utils.get_redirect_url(request)},
                                    context_instance=RequestContext(request))

    elif request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        remember_me = request.POST.get("remember_me", None)
        try:
            user_inst = User.login(email, password)
        except User.LoginEmailDoesNotExist, e: 
            return render_to_response(template,
                                      {'email' : email,
                                       'remember_me' : remember_me,
                                       'error_msg' : web_text.LOGIN_WRONG_EMAIL
                                      },
                                      context_instance=RequestContext(request))
        except User.LoginPasswordIncorrect, e:
            return render_to_response(template,
                                      {'email' : email,
                                       'remember_me' : remember_me,
                                       'error_msg' : web_utils.LOGIN_WRONG_PASSWORD
                                      },
                                      context_instance=RequestContext(request))
        user_context = user_inst.read()
        user = authenticate(username = user_context['username'], password = password)
        if not user.is_active:
            return render_to_response(template,
                                      {'email' : email,
                                       'remember_me' : remember_me,
                                       'error_msg' : web_utils.LOGIN_USER_NOT_ACTIVE
                                      },
                                      context_instance=RequestContext(request))
        auth_login(request, user)
        if not remember_me:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        print redirect_url
        return HttpResponseRedirect(redirect_url)
