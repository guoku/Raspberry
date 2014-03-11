#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.entity import Entity
from base.taobao_shop import TaobaoShop
from base.user import User
from base.taobao_shop import TaobaoShop

from forms import ShopVerificationForm
import re
from web import web_utils
from utils.authority import seller_only
from utils.extractor.taobao import TaobaoExtractor 
from urlparse import urlparse

@require_GET
@login_required
@seller_only
def index(request, user_context, shop_inst):
    verification_form = ShopVerificationForm()
    shop_context = shop_inst.read()
    shop_verification = shop_inst.read_shop_verification()
    return render_to_response(
        "index.html",
        { 
            "user_context" : user_context,
            "shop_context" : shop_context,
            "verification_form" : verification_form,
            "shop_verification" : shop_verification
        },
        context_instance=RequestContext(request)
    )
    #return HttpResponseRedirect(reverse('seller_commodities'))

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
                "user_context" : request_user_context 
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
            taobao_item_info = TaobaoExtractor.fetch_item(taobao_id)
            nick = taobao_item_info['nick']
            if request_user_context.get('taobao_nick') == nick:
                user_inst.create_seller_info(nick)
                if not TaobaoShop.nick_exist(nick):
                    shop_info = TaobaoExtractor.fetch_shop(taobao_item_info['shop_link'])
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
                return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))
        else:
            return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))

