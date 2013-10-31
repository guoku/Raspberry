#coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from common.category import RBCategory
from mango.client import MangoApiClient
import datetime
import json

def sync_category(request):
    _all_categories = RBCategory.all_group_with_full_category()
    return HttpResponse(json.dumps(_all_categories))

def sync_taobao_item(request):
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '100'))
    
    _mango_client = MangoApiClient()
    _taobao_id_list = _mango_client.find_item(
        offset = _offset,
        count = _count
    )
    return HttpResponse(json.dumps(_taobao_id_list))
