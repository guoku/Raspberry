#coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from common.category import RBCategory
from common.entity import RBEntity
from mango.client import MangoApiClient
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
import datetime
import json

def sync_category(request):
    _all_categories = RBCategory.all_group_with_full_category()
    return SuccessJsonResponse(_all_categories)

def sync_taobao_item(request):
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '100'))
    
    _mango_client = MangoApiClient()
    _taobao_id_list = _mango_client.find_item(
        offset = _offset,
        count = _count
    )
    return SuccessJsonResponse(_taobao_id_list)

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
            
        _entity_id = RBEntity.check_taobao_item_exist(_taobao_id)
        if _entity_id == None:
            _entity = RBEntity.create_by_taobao_item(
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
                'status' : 'success'
            }
            return SuccessJsonResponse(_rslt)
        else:
            _rslt = {
                'message' : 'item_exist', 
                'status' : 'failed'
            }
            return SuccessJsonResponse(_rslt)

