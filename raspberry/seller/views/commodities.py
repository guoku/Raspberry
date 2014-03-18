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
from forms import GuokuPlusApplicationForm, ShopVerificationForm 
from utils.authority import seller_only

@require_GET
@login_required
@seller_only
def commodities(request, user_context, shop_inst):
    item_list = Item.find_taobao_item(shop_nick = user_context['shop_nick'], full_info = True) 
    for i in range(len(item_list)):
        item = Item(item_list[i]['item_id'])
        item_list[i]['item'] = item.read()
    verification_form = ShopVerificationForm()
    shop_context = shop_inst.read()
    if not shop_context['shop_verified']:
        shop_verification = shop_inst.read_shop_verification()
    else:
        shop_verification = None
    print verification_form.as_table()
    return render_to_response("commodities.html",
                              {"item_list": item_list,
                               "user_context": user_context,
                               "verification_form" : verification_form,
                               "shop_verification" : shop_verification},
                              context_instance=RequestContext(request))

@require_POST
@login_required
@seller_only
def verify(request, user_context, shop_inst):
    shop_context = shop_inst.read()
    form = ShopVerificationForm(request.POST)
    if form.is_valid():
        verification = shop_inst.read_shop_verification()
        if not verification:
            shop_inst.create_verification_info(
                shop_type = form.cleaned_data['shop_type'],
                company_name = form.cleaned_data['company_name'],
                email = form.cleaned_data['email'],
                mobile = form.cleaned_data['mobile'],
                qq_account = form.cleaned_data['qq_account'],
                main_products = form.cleaned_data['main_products'],
                intro = form.cleaned_data['intro']
            )
        else:
            shop_inst.update_verification_info(
                shop_type = form.cleaned_data['shop_type'],
                company_name = form.cleaned_data['company_name'],
                email = form.cleaned_data['email'],
                mobile = form.cleaned_data['mobile'],
                qq_account = form.cleaned_data['qq_account'],
                main_products = form.cleaned_data['main_products'],
                intro = form.cleaned_data['intro']
            )     
        return HttpResponseRedirect(reverse('seller_index'))
    return HttpResponse(form.errors)

@require_GET
@login_required
@seller_only
def guokuplus_list(request, user_context, shop_inst):
    items = shop_inst.read_guoku_plus_application_list()
    return render_to_response("guoku_plus_list.html",
                    {'items' : items},
                    context_instance = RequestContext(request))

@require_GET
@login_required
@seller_only
def guoku_plus_activity_list(request, user_context, shop_inst):
    pass    
