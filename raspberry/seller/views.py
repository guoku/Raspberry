from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext

from base.entity import Entity
from base.taobao_shop import TaobaoShop
from base.user import User
from base.item import Item

def index(request):
    pass

def commodities(request):
    user_id = request.user.id
    user_inst = User(user_id)
    if request.method == "GET":
        user_context = user_inst.read()
        item_list = Item.find_taobao_item(shop_nick = user_context['shop_nick'], full_info = True) 
        for i in range(len(item_list)):
            print item_list[i]
            item = Item(item_list[i]['item_id'])
            item_list[i]['item'] = item.read()
        
        return render_to_response("commodities.html",
                                  {"item_list": item_list,
                                   "user_context": user_context},
                                  context_instance=RequestContext(request))

def verify(request):
    if request.method == "POST":
        intro = request.POST.get("intro", "")
        user_inst = User(request.user.id)
        user_context = user_inst.read()
        shop_nick = user_context.get("shop_nick", None)
        if shop_nick:
            shop = TaobaoShop(shop_nick)
            shop.create_verification_info(intro)
        else:
            pass
    pass

def apply_guoku_price(request):
    if request.method == "POST":
        user_inst = User(request.user.id)
        user_context = user_inst.read()
        shop_nick = user_context.get("shop_nick", None)
        if shop_nick:
            taobao_item_id = request.POST["taobao_item_id"]
            quantity = int(request.POST["quantity"])
            original_price = float(request.POST['original_price'])
            sale_price = float(request.POST['sale_price'])
            duration = int(request.POST['duration'])       
            shop = TaobaoShop(shop_nick)
            shop.create_guoku_price_application(taobao_item_id, quantity, original_price, sale_price, duration)
            return HttpResponse("OK")   
        else:
            pass
    else:
        pass

