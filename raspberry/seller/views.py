from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext

from base.entity import Entity
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
