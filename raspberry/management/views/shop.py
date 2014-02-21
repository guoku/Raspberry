#coding=utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from base.taobao_shop import TaobaoShop
from base.item import Item
from base.entity import Entity
from utils.authority import staff_only 
from utils.paginator import Paginator
from utils import fetcher

NUM_EVERY_PAGE = 100
ALL_GIFTS = [u"果库福利", u"应用市场活动", u"微博微信活动"]
SHOP_TYPES = ["taobao.com", "tmall.com", "global"]

@require_GET
@login_required
@staff_only
def index(request):
    return HttpResponseRedirect(reverse('management_shop_list'))

@require_GET
@login_required
@staff_only
def shop_list(request):
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

@require_POST
@login_required
@staff_only
def add_shop(request):
    _shop_link = request.POST.get("shop_link", None)
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

@require_GET
@login_required
@staff_only
def shop_detail(request):
    _nick = request.GET.get("nick", None)
    if _nick:
        shop = TaobaoShop(_nick)
        shop_context = shop.read()
        item_list = Item.find_taobao_item(shop_nick =shop_context['shop_nick'], full_info=True) 
        items = []
        for item in item_list:
            inst = Item(item['item_id'])
            item_context = inst.read()
            entity = Entity(item['entity_id'])
            item_context['image'] = entity.read()['chief_image']
            items.append(item_context)
        return render_to_response("shop/detail.html",
                                  { "shop" : shop_context,
                                    "items" : items,
                                    "gifts" : ALL_GIFTS,
                                    "priorities" : range(11),
                                    "taobao_shop_types" : SHOP_TYPES 
                                  },
                                  context_instance = RequestContext(request))
    else:
        return Http404()

@require_POST
@login_required
@staff_only
def edit_shop(request):
    _nick = request.POST.get("nick", None)
    if _nick:
        _priority = int(request.POST.get('priority', '10'))
        _cycle = int(request.POST.get('cycle', '720'))
        _shop_type = request.POST.get('shoptype', 'taobao.com')
        _orientational = request.POST.get('orientational', 'false')
        if _orientational == "false":
            _orientational = False
        else:
            _orientational = True
        _commission_rate = float(request.POST.get("commission_rate", "-1"))
        _original = request.POST.get('original', 'false')
        if _original == "false":
            _original = False
        else:
            _original = True
        _gifts = request.POST.getlist("gifts")
        _commission = request.POST.get('commission', 'false')
        if _commission == "false":
            _commission = False
        else:
            _commission = True
        _single_tail = request.POST.get('single_tail', 'false')
        if _single_tail == "false":
            _single_tail = False
        else:
            _single_tail = True

        _main_products = request.POST.get('main_products', "")
        shop = TaobaoShop(_nick)
        shop.update(priority = _priority,
                    cycle = _cycle,
                    shop_type =_shop_type,
                    orientational = _orientational,
                    commission = _commission,
                    commission_rate = _commission_rate,
                    original = _original,
                    gifts = _gifts,
                    main_products = _main_products,
                    single_tail = _single_tail)
        return HttpResponseRedirect(reverse("management_shop_detail") + "?nick=" + _nick)
    else:
        return Http404()

@require_GET
@login_required
@staff_only
def guokuplus_list(request):
    GuokuPlusApplication.objects.all()
    pass

@login_required
@staff_only
def guokuplus_item_update(request):
    pass
