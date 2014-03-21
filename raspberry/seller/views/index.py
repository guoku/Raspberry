#coding=utf-8

from django.contrib import messages
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
from utils.taobao import  is_taobao_url, parse_taobao_id_from_url
from utils.extractor.taobao import TaobaoExtractor 
from urlparse import urlparse
from seller.views.seller_utils import get_guoku_plus_item_context, NotTaobaoUrl, NotSellerOwnProduct,InvalidUrl 

@require_GET
@login_required
@seller_only
def index(request, user_context, shop_inst):
    shop_context = shop_inst.read()
    shop_verification = shop_inst.read_shop_verification()
    verification_form = ShopVerificationForm(
        {
            "user_context" : user_context,
            "shop_type" : shop_context.get('shop_type', None),
            "qq_account" : shop_context.get('shop_qq_account', None),
            "email" : shop_context.get('shop_email', None),
            "company_name" : shop_context.get('shop_company_name', None),
            "mobile" : shop_context.get('shop_mobile', None),
            "main_products" : shop_context.get('shop_main_products', None),
            "intro" : shop_context.get('shop_intro', None)
        }
    )
    shop_context = shop_inst.read()
    shop_verification = shop_inst.read_shop_verification()
    application_form = GuokuPlusApplicationForm()
    guokuplus_list, total = GuokuPlusActivity.find(shop_nick = user_context['shop_nick'])
    return render_to_response(
        "index.html",
        { 
            "user_context" : user_context,
            "shop_context" : shop_context,
            "application_form" : application_form,
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
        taobao_nick = request_user_context.get("taobao_nick", None)
        taobao_shop = None
        if taobao_nick and TaobaoShop.nick_exist(taobao_nick):
            taobao_shop = TaobaoShop(taobao_nick).read()
        return render_to_response(
            "bind_taobao_shop.html",
            { 
                "user_context" : request_user_context, 
                "taobao_shop" : taobao_shop
            },
            context_instance=RequestContext(request)
        )
    elif request.method == "POST":
        if not request_user_context.get("taobao_nick"):
            messages.info(request, u"尚未绑定淘宝帐号") 
            return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))
        item_url = request.POST.get('item_url', None)
        if not item_url:
            message.info(request, u"请输入商品地址")
            return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))
      
        if is_taobao_url(item_url):
            taobao_id = parse_taobao_id_from_url(item_url)
            taobao_item_info = TaobaoExtractor.fetch_item(taobao_id)
            nick = taobao_item_info['nick'].decode("utf-8")
            user_taobao_nick = request_user_context.get('taobao_nick')
            if user_taobao_nick == nick:
                user_inst.create_seller_info(nick)
                if not TaobaoShop.nick_exist(nick):
                    shop_info = TaobaoExtractor.fetch_shop(taobao_item_info['shop_link'])
                    TaobaoShop.create(
                        shop_info['nick'],
                        shop_info['shop_id'],
                        shop_info['title'],
                        shop_info['type'],
                        shop_info['seller_id'],
                        shop_info['pic']
                    ) 
                return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))
            else:
                messages.info(request, u"错误的商品地址，请输入淘宝商品地址")
                return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))
        else:
            return HttpResponseRedirect(reverse('seller_bind_taobao_shop'))

@require_POST
@login_required
def confirm_current_taobao_shop(request):
    user_inst = User(request.user.id)
    user_context = user_inst.read()
    if user_context['taobao_nick']:
        user_inst.create_seller_info(user_context['taobao_nick'])
    return HttpResponseRedirect(reverse('seller_index'))

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
        total_volume = form.cleaned_data["total_volume"]
        sale_price = form.cleaned_data['sale_price']
        seller_remarks = form.cleaned_data['seller_remarks']
        if item_context['price'] < sale_price:
            return HttpResponse(u"优惠价不能大于原价")
        GuokuPlusActivity.create(item_context['taobao_id'], sale_price, total_volume, seller_remarks, item_context['shop_nick'])
        return HttpResponseRedirect(reverse("seller_index"))
    return HttpResponse(form.errors)

@require_POST
@seller_only
def verify_guoku_plus_token(request, user_context, shop_inst):
    token = request.POST.get("token", None)
    if token:
        result = GuokuPlusActivity.use_token(token)
        return HttpResponse(result)

@require_GET
def faq(request):
    return render_to_response("faq.html")


@require_POST
@login_required
def verify_token(request):
    token = request.POST.get("token", None)
    quantity = int(request.POST.get("quantity", "1"))
    print token, quantity
    if token and quantity >= 1:
        guokuplus = GuokuPlusActivity.get_activity_by_token(token)
        status = guokuplus.use_token(token, quantity)
        return HttpResponse(status)
    return HttpResponse("error")
