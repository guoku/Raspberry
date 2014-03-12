#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.entity import Entity
from base.taobao_shop import TaobaoShop, GuokuPlusActivity
from base.user import User
from base.taobao_shop import TaobaoShop

from forms import ShopVerificationForm, GuokuPlusApplicationForm
import re
from web import web_utils
from utils.authority import seller_only
from utils.extractor.taobao import TaobaoExtractor 
from urlparse import urlparse
from seller.views.seller_utils import get_guoku_plus_item_context, NotTaobaoUrl, NotSellerOwnProduct,InvalidUrl 

@require_GET
@login_required
@seller_only
def index(request, user_context, shop_inst):
    verification_form = ShopVerificationForm()
    shop_context = shop_inst.read()
    shop_verification = shop_inst.read_shop_verification()
    application_form = GuokuPlusApplicationForm()
    guokuplus_list = GuokuPlusActivity.find(shop_nick = user_context['shop_nick'])
    return render_to_response(
        "index.html",
        { 
            "user_context" : user_context,
            "shop_context" : shop_context,
            "verification_form" : verification_form,
            "shop_verification" : shop_verification,
            "guokuplus_list" : guokuplus_list
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


@require_POST
@login_required
@seller_only
def apply_guoku_plus(request, user_context, shop_inst):
    form = GuokuPlusApplicationForm(request.POST)
    if form.is_valid():
        taobao_url = form.cleaned_data["taobao_url"]
        try:
            item_context = get_guoku_plus_item_context(taobao_url, user_context['shop_nick'], user_context['user_id'])
        except NotTaobaoUrl, e:
            return HttpResponse(str(e))
        except NotSellerOwnProduct, e:
            return HttpResponse(str(e))
        except InvalidUrl, e:
            return HttpResponse(str(e))
        total_ = form.cleaned_data["quantity"]
        sale_price = form.cleaned_data['sale_price']
        seller_remarks = form.cleaned_data['remarks']
        if item_context['price'] < sale_price:
            return HttpResponse("sale price must less that original price")
        GuokuPlusActivity.create(taobao_item_id, total_volume, sale_price, seller_remarks)
        return HttpResponseRedirect(reverse("seller_index"))
    return HttpResponse("error")

@require_POST
@seller_only
def verify_guoku_plus_token(request, user_context, shop_inst):
    pass
