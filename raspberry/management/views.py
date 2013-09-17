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

from common.category import RBCategory
from common.entity import RBEntity
from common.item import RBItem

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
        _cid = int(request.GET.get("cid", "1"))
        _category_list = RBCategory.find()
        return render_to_response(
            "entity/new.html", 
            {
                'selected_category_id' : _cid,
                'category_list' : _category_list
            },
            context_instance=RequestContext(request)
        )
    else: 
        _cand_url = request.POST.get("url", None)
        _selected_category_id = int(request.POST.get("category_id", "1"))
        _hostname = urlparse(_cand_url).hostname
        if re.search(r"\b(tmall|taobao)\.com$", _hostname) != None: 
            _taobao_id = _parse_taobao_id_from_url(_cand_url)

            _entity_id = RBEntity.check_taobao_item_exist(_taobao_id)
            if _entity_id == None:
                _taobao_item_info = _load_taobao_item_info(_taobao_id)
                return render_to_response( 
                    'entity/create.html', 
                    {
                      'taobao_id' : _taobao_id,
                      'cid' : _taobao_item_info['cid'], 
                      'taobao_title' : _taobao_item_info['title'], 
                      'shop_nick' : _taobao_item_info['shop_nick'], 
                      'price' : _taobao_item_info['price'], 
                      'thumb_images' : _taobao_item_info["thumb_images"],
                      'soldout' : 0, 
                      'selected_category_id' : _selected_category_id, 
                      'category_list' : RBCategory.find(), 
                    },
                    context_instance = RequestContext(request)
                )
                
@login_required
def create_entity_by_taobao_item(request):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _taobao_soldout = request.POST.get("taobao_soldout", None)
        _image_url = request.POST.get("image_url", None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = request.POST.get("intro", None)
        _category_id = int(request.POST.get("category_id", None))
        
        _entity = RBEntity.create_by_taobao_item(
            creator_id = request.user.id,
            category_id = _category_id,
            taobao_id = _taobao_id,
            image_url = _image_url,
            brand = _brand,
            title = _title,
            intro = _intro,
            cid = _cid,
            taobao_title = _taobao_title,
            taobao_shop_nick = _taobao_shop_nick,
            taobao_price = _taobao_price,
            taobao_soldout = _taobao_soldout,
        )

        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))

@login_required
def edit_entity(request, entity_id):
    if request.method == 'GET':
        _entity_context = RBEntity(entity_id).read()
        _item_context_list = RBItem.read_items(_entity_context['base_info']['item_id_list'])
        return render_to_response( 
            'entity/edit.html', 
            {
              'entity_context' : _entity_context,
              'category_list' : RBCategory.find(), 
              'item_context_list' : _item_context_list,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = request.POST.get("intro", None)
        _category_id = int(request.POST.get("category_id", None))
        _entity = RBEntity(entity_id)
        _entity.update(
            category_id = _category_id,
            brand = _brand,
            title = _title,
            intro = _intro
        )
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : entity_id })) 

        

@login_required
def entity_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _category_groups = RBCategory.allgroups()
        _category_id = int(request.GET.get("cid", "1"))
        _category_obj = RBCategory.get(_category_id)
        _categories = RBCategory.find(group_id = _category_obj['group_id'])
         
    
        _entity_id_list = RBEntity.find(_category_id)
        _entity_context_list = RBEntity.read_entities(_entity_id_list)
        
        return render_to_response( 
            'entity/list.html', 
            {
                'category_obj' : _category_obj,
                'category_groups' : _category_groups,
                'categories' : _categories,
                'entity_context_list' : _entity_context_list,
            },
            context_instance = RequestContext(request)
        )
    else:
        _categories = RBCategory.find(group_id = int(_group_id))
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_categories[0]['id'])) 

@login_required
def unbind_entity_item(request, entity_id, item_id):
    _entity = RBEntity(entity_id)
    _entity.unbind_item(item_id)

    return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))

@login_required
def load_taobao_item_for_entity(request, entity_id):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
            
        _entity_id = RBEntity.check_taobao_item_exist(_taobao_id)
        if _entity_id == None:
            _taobao_item_info = _load_taobao_item_info(_taobao_id)
            return render_to_response( 
                'entity/taobao_item_info.html', 
                {
                  'entity_id' : entity_id,
                  'taobao_id' : _taobao_id,
                  'cid' : _taobao_item_info['cid'], 
                  'taobao_title' : _taobao_item_info['title'], 
                  'shop_nick' : _taobao_item_info['shop_nick'], 
                  'price' : _taobao_item_info['price'], 
                  'thumb_images' : _taobao_item_info["thumb_images"],
                  'soldout' : 0, 
                },
                context_instance = RequestContext(request)
            )
    
@login_required
def add_taobao_item_for_entity(request, entity_id):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _taobao_soldout = request.POST.get("taobao_soldout", None)
            
    
        _entity = RBEntity(entity_id)
        _entity.add_taobao_item(
            taobao_id = _taobao_id,
            cid = _cid,
            taobao_title = _taobao_title,
            taobao_shop_nick = _taobao_shop_nick,
            taobao_price = _taobao_price,
            taobao_soldout = _taobao_soldout,
        ) 
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))
