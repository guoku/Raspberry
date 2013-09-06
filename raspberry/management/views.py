# coding=utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
from taobaoapi.utils import load_taobao_item_info_from_api
from taobaoapi.client import TaobaoApiClient
import HTMLParser
import re 
import datetime
import time
import json

from common.entity import RBEntity

def _parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None

def _load_taobao_item_info(taobao_id):
    taobao_item_info = load_taobao_item_info_from_api(taobao_id)
    thumb_images = []
    image_url = None
    for thumb_img in taobao_item_info["item_imgs"]["item_img"]:
        thumb_images.append(thumb_img["url"])
    taobao_item_info["thumb_images"] = thumb_images
    taobao_item_info["title"] = HTMLParser.HTMLParser().unescape(taobao_item_info["title"])
    
    location = taobao_item_info['location']
    if location['city'] == location['state']:
        location = location['city']
    else:
        location = "%s %s" % (location['state'], location['city'])
    taobao_item_info["location"] = location
    taobao_item_info["shop_nick"] = taobao_item_info["nick"] 
    return taobao_item_info 

@login_required
def new_entity(request):
    if request.method == 'GET':
        return render_to_response(
            "management/entity/new.html", 
            context_instance=RequestContext(request)
        )
    else: 
        _cand_url = request.POST.get("url", None)
        _hostname = urlparse(_cand_url).hostname
        if re.search(r"\b(tmall|taobao)\.com$", _hostname) != None: 
            _taobao_id = _parse_taobao_id_from_url(_cand_url)

            _entity_id = RBEntity.check_taobao_item_exist(_taobao_id)
            if _entity_id == None:
                _taobao_item_info = _load_taobao_item_info(_taobao_id)
                return render_to_response( 
                    'management/entity/create.html', 
                    {
                      'taobao_id' : _taobao_id,
                      'taobao_category_id' : _taobao_item_info['cid'], 
                      'taobao_title' : _taobao_item_info['title'], 
                      'shop_nick' : _taobao_item_info['shop_nick'], 
                      'price' : _taobao_item_info['price'], 
                      'thumb_images' : _taobao_item_info["thumb_images"],
                      'soldout' : 0, 
                    },
                    context_instance = RequestContext(request)
                )
                
#@login_required
def create_entity_by_taobao_item(request):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _taobao_category_id = request.POST.get("taobao_category_id", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _taobao_soldout = request.POST.get("taobao_soldout", None)
        _image_url = request.POST.get("image_url", None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
            
        _mango_client = MangoApiClient()
        _entity_id = _mango_client.create_entity_by_taobao_item(
            taobao_id = _taobao_id,
            brand = _brand,
            title = _title,
            taobao_category_id = _taobao_category_id,
            taobao_title = _taobao_title,
            taobao_shop_nick = _taobao_shop_nick,
            taobao_price = _taobao_price,
            taobao_soldout = _taobao_soldout,
        )

        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity_id }))

