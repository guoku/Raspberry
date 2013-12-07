#coding=utf-8
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from base.category import Category
from base.entity import Entity
from base.item import Item
from base.models import Entity as EntityModel
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
import datetime
import json

def sync_category(request):
    _all_categories = Category.all_group_with_full_category()
    return SuccessJsonResponse(_all_categories)

def sync_taobao_item(request):
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '100'))
    
    _taobao_id_list = Item.find(
        offset = _offset,
        count = _count,
        full_info = True
    )
    return SuccessJsonResponse(_taobao_id_list)


def sync_entity_without_title(request):
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '100'))
    
    _rslt = []
    for _entity_obj in EntityModel.objects.filter(Q(title__isnull = True) | Q(title = '')).filter(id__gt = 210000)[_offset : _offset + _count]:
        try:
            _context = { 
                'entity_id' : _entity_obj.id,
                'item_titles' : []
            }
            for _item_id in Item.find(entity_id = _entity_obj.id):
                _context['item_titles'].append(Item(_item_id).read()['title'])
            _rslt.append(_context)
        except Exception, e:
            print e
    
    return SuccessJsonResponse(_rslt)

def sync_update_entity_title(request, entity_id):
    if request.method == 'POST':
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        
        _entity = Entity(entity_id)
        _entity.update(
            brand = _brand,
            title = _title
        )
        _rslt = {
            'status' : 'success'
        }
        return SuccessJsonResponse(_rslt)



def create_entity_from_offline(request):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _taobao_soldout = request.POST.get("taobao_soldout", '0')
        if _taobao_soldout == '0':
            _taobao_soldout = False
        else:
            _taobao_soldout = True
        _chief_image_url = request.POST.get("chief_image_url", None)
        _brand = request.POST.get("brand", "")
        _title = request.POST.get("title", "")
        _intro = request.POST.get("intro", "")
        _category_id = int(request.POST.get("category_id", None))
        _detail_image_urls = request.POST.getlist("image_url")
        
        if _chief_image_url in _detail_image_urls:
            _detail_image_urls.remove(_chief_image_url)
            
        _item = Item.get_item_by_taobao_id(_taobao_id)
        if _item == None:
            _entity = Entity.create_by_taobao_item(
                creator_id = request.user.id,
                category_id = _category_id,
                chief_image_url = _chief_image_url,
                taobao_item_info = {
                    'taobao_id' : _taobao_id,
                    'cid' : _cid,
                    'title' : _taobao_title,
                    'shop_nick' : _taobao_shop_nick,
                    'price' : _taobao_price,
                    'soldout' : _taobao_soldout 
                },
                brand = _brand,
                title = _title,
                intro = _intro,
                detail_image_urls = _detail_image_urls,
                weight = -1,
            )
            _rslt = {
                'entity_id' : _entity.entity_id,
                'item_id' : _entity.read()['item_id_list'][0],
                'status' : 'success'
            }
            return SuccessJsonResponse(_rslt)
        else:
            _rslt = {
                'message' : 'item_exist',
                'item_id' : _item.item_id,
                'status' : 'failed'
            }
            return SuccessJsonResponse(_rslt)

