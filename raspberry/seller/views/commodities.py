#coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseForbidden
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
        form = ShopVerificationForm(request.POST)
        if form.is_valid():
            shop_inst.create_verification_info(
                user_id = request.user.id,
                shop_type = form.cleaned_data['shop_type'],
                company_name = form.cleaned_data['company_name'],
                email = form.cleaned_data['email'],
                mobile = form.cleaned_data['mobile'],
                qq_account = form.cleaned_data['qq_account'],
                main_products = form.cleaned_data['main_products'],
                intro = form.cleaned_data['intro']
            )
        return HttpResponseRedirect()

@require_http_methods(["GET", "POST"])
@login_required
@seller_only
def apply_guoku_plus(request, user_context, shop_inst):
    if request.method == "POST":
        form = GuokuPlusApplicationForm(request.POST)
        if form.is_valid():
            taobao_item_id = form.cleaned_data["taobao_item_id"]
            item_inst = Item.get_item_by_taobao_id(taobao_item_id)
            item_context = item_inst.read()
            if shop_inst.item_exist(taobao_item_id):
                quantity = form.cleaned_data["quantity"]
                sale_price = form.cleaned_data['sale_price']
                remarks = form.cleaned_data['remarks']
                shop_inst.create_guoku_plus_application(taobao_item_id, item_context['entity_id'], quantity, sale_price, remarks)
                return HttpResponseRedirect(reverse("seller_guoku_plus_applications_list"))
            else:
                return HttpResponseForbidden()
        return render_to_response("guoku_plus_application.html",
                                  { "form" : form },
                                  context_instance = RequestContext(request))
    elif request.method == "GET":
        taobao_item_id = request.GET.get('taobao_id', None)
        if shop_inst.item_exist(taobao_item_id):
            item = Item.get_item_by_taobao_id(taobao_item_id)
            item_context = item.read()
            form = GuokuPlusApplicationForm({"taobao_item_id" : taobao_item_id, 'original_price': item_context['price']})
            return render_to_response("guoku_plus_application.html",
                                      {"form" : form,
                                       "taobao_item": item_context},
                                      context_instance = RequestContext(request)) 
        else:
            return HttpResponseForbidden()
        

@require_GET
@login_required
@seller_only
def guoku_plus_applications_list(request, user_context, shop_inst):
    items = shop_inst.read_guoku_plus_application_list()
    return render_to_response("guoku_plus_application_list.html",
                    {'items' : items},
                    context_instance = RequestContext(request))
