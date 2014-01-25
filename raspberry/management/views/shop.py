#coding=utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.taobao_shop import TaobaoShop
from base.item import Item
from base.entity import Entity
from utils.authority import staff_only 
from utils.paginator import Paginator
from utils import fetcher

NUM_EVERY_PAGE = 100
ALL_GIFTS = [u"果库福利", u"应用市场活动", u"微博微信活动"]
SHOP_TYPES = ["taobao.com", "tmall.com", "global"]

@login_required
@staff_only
def index(request):
    return HttpResponseRedirect(reverse('management_shop_list'))

@login_required
@staff_only
def shop_list(request):
    if request.method == "GET":
        _para = {}
        _p = int(request.GET.get("p", 1))
        _nick = request.GET.get("nick", None)
        if _nick: 
            _para['nick'] = unicode(_nick)
        
        _sort_by = request.GET.get("sort_by", "-created_time")
        if _sort_by:
            _sort_on = _sort_by
            _para['sort_by'] = _sort_by
            _order = request.GET.get("order", "asc")
            _para['order'] = _order
            if _sort_by == "priority":
                _sort_on = "crawler_info.priority"
            elif _sort_by == "commission_rate":
                _sort_on = "extended_info.commission_rate"
            else:
                _sort_on = _sort_by
            if _order == "desc":
                _sort_on = "-" + _sort_on
        else:
            _sort_on = "-created_time"
            _sort_by = "created_time"
            _order = "desc"

        _gifts = request.GET.getlist("gifts")
        if _gifts:
            _para['gifts'] = _gifts
        _offset = NUM_EVERY_PAGE * (_p - 1)
        _shops, _count = TaobaoShop.find(_nick, _offset, NUM_EVERY_PAGE, _sort_on, _gifts)
        _paginator = Paginator(_p, NUM_EVERY_PAGE, _count, _para) 
        
        return render_to_response('shop/list.html', 
                                  {
                                    'shops': _shops,
                                    'sort_by' : _sort_by,
                                    'order' : _order,
                                    'gifts' : _gifts,
                                    'all_gifts' : ALL_GIFTS,
                                    'paginator' : _paginator
                                  },
                                  context_instance = RequestContext(request))
    else:
        pass

@login_required
@staff_only
def add_shop(request):
    if request.method == "POST":
        print request.POST
        _shop_link = request.POST.get("shop_link", None)
        print _shop_link
        if _shop_link:
            _shop_info = fetcher.fetch_shop(_shop_link)
            
            if not TaobaoShop.nick_exist(_shop_info['nick']):
                TaobaoShop.create(nick = _shop_info['nick'],
                              shop_id = _shop_info['shop_id'],
                              seller_id = _shop_info['seller_id'],
                              title = _shop_info['title'],
                              shop_type = _shop_info['type'],
                              pic_path = _shop_info['pic'])
            else:
                messages.info(request, "该店铺已经存在")
            return HttpResponseRedirect(reverse("management_shop_list"))
    else:
        pass

@login_required
@staff_only
def shop_detail(request):
    if request.method == "GET":
        _nick = request.GET.get("nick", None)
        if _nick:
            shop = TaobaoShop(_nick)
            shop_context = shop.read()
            print shop_context
            item_list = Item.find_taobao_item(shop_nick =shop_context['shop_nick'], full_info=True) 
            items = []
            for item in item_list:
                inst = Item(item['item_id'])
                item_context = inst.read()
                entity = Entity(item['entity_id'])
                item_context['image'] = entity.read()['chief_image']
                items.append(item_context)
            print 'len', len(items)
            return render_to_response("shop/detail.html",
                                      { "shop" : shop_context,
                                        "items" : items,
                                        "gifts" : ALL_GIFTS,
                                        "priorities" : range(11),
                                        "taobao_shop_types" : SHOP_TYPES 
                                      },
                                      context_instance = RequestContext(request))
            
    return HttpResponse("OK")
