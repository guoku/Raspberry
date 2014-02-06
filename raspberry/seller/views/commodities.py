#coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from base.entity import Entity
from base.taobao_shop import TaobaoShop
from base.user import User
from base.item import Item
from forms import GuokuPlusApplicationForm
from utils.authority import seller_only

@require_GET
@login_required
@seller_only
def index(request, user_context, shop_inst):
    return HttpResponseRedirect(reverse('seller_commodities'))


@require_GET
@login_required
@seller_only
def commodities(request, user_context, shop_inst):
    item_list = Item.find_taobao_item(shop_nick = user_context['shop_nick'], full_info = True) 
    for i in range(len(item_list)):
        item = Item(item_list[i]['item_id'])
        item_list[i]['item'] = item.read()
    
    return render_to_response("commodities.html",
                              {"item_list": item_list,
                               "user_context": user_context},
                              context_instance=RequestContext(request))

@require_http_methods(["GET", "POST"])
@login_required
@seller_only
def verify(request, user_context, shop_inst):
    if request.method == "POST":
        intro = request.POST.get("intro", "")
        shop_inst.create_verification_info(intro)

@login_required
@seller_only
def apply_guoku_plus(request, user_context, shop_inst):
    if request.method == "POST":
        taobao_item_id = request.POST["taobao_item_id"]
        quantity = int(request.POST["quantity"])
        original_price = float(request.POST['original_price'])
        sale_price = float(request.POST['sale_price'])
        duration = int(request.POST['duration'])       
        shop_inst.create_guoku_plus_application(taobao_item_id, quantity, original_price, sale_price, duration)
        return HttpResponse("OK")   
    elif request.method == "GET":
        taobao_id = request.GET.get('taobao_id', None) 
    else:
        pass

@login_required
@seller_only
def guoku_plus_list(request, user_context, shop_inst):
    pass
