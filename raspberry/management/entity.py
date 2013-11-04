#coding=utf-8
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

from common.candidate import RBCandidate
from common.category import RBCategory
from common.entity import RBEntity
from common.item import RBItem
from common.note import RBNote
from common.user import RBUser
from utils.paginator import Paginator

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
                'active_division' : 'entity',
                'selected_category_id' : _cid,
                'category_list' : _category_list
            },
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
                _selected_category_id = int(request.POST.get("category_id", "1"))
                _brand = ''
                _title = ''
                
                _candidate_id = request.POST.get("candidate_id", None)
                if _candidate_id != None:
                    _candidate_context = RBCandidate(_candidate_id).read()
                    _brand = _candidate_context['brand']
                    _title = _candidate_context['title']
                    if _candidate_context['category_id'] != 0:
                        _selected_category_id = _candidate_context['category_id']
                    _note_context = RBNote(_candidate_context['note_id']).read()
                    _note_creator_context = RBUser(_note_context['creator_id']).read()

                else:
                    _candidate_context = None
                    _note_context = None
                    _note_creator_context = None
                
                return render_to_response( 
                    'entity/create.html', 
                    {
                        'active_division' : 'entity',
                        'taobao_id' : _taobao_id,
                        'cid' : _taobao_item_info['cid'], 
                        'taobao_title' : _taobao_item_info['title'], 
                        'shop_nick' : _taobao_item_info['shop_nick'], 
                        'price' : _taobao_item_info['price'], 
                        'thumb_images' : _taobao_item_info["thumb_images"],
                        'selected_category_id' : _selected_category_id, 
                        'category_list' : RBCategory.find(),
                        'brand' : _brand,
                        'title' : _title,
                        'candidate_context' : _candidate_context,
                        'note_context' : _note_context,
                        'note_creator_context' : _note_creator_context
                    },
                    context_instance = RequestContext(request)
                )
            else:
                return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity_id }) + '?code=1')
                
                
@login_required
def create_entity_by_taobao_item(request):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _chief_image_url = request.POST.get("chief_image_url", None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = request.POST.get("intro", None)
        _category_id = int(request.POST.get("category_id", None))
        _candidate_id = request.POST.get("candidate_id", None)
        if _candidate_id != None:
            _candidate_id = int(_candidate_id)
        _detail_image_urls = request.POST.getlist("image_url")
        
        if _chief_image_url in _detail_image_urls:
            _detail_image_urls.remove(_chief_image_url)
        
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
                'soldout' : False,
            },
            brand = _brand,
            title = _title,
            intro = _intro,
            detail_image_urls = _detail_image_urls,
            candidate_id = _candidate_id
        )

        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))

@login_required
def edit_entity(request, entity_id):
    if request.method == 'GET':
        _code = request.GET.get("code", None)
        if _code == "1":
            _message = "淘宝商品已被创建至本entity" 
        else:
            _message = None
        _entity_context = RBEntity(entity_id).read()
        _item_context_list = []
        for _item_id in _entity_context['item_id_list']:
            _item_context_list.append(RBItem(_item_id).read())
        return render_to_response( 
            'entity/edit.html', 
            {
                'active_division' : 'entity',
                'entity_context' : _entity_context,
                'category_list' : RBCategory.find(), 
                'item_context_list' : _item_context_list,
                'message' : _message
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = request.POST.get("intro", None)
        _price = request.POST.get("price", None)
        _weight = int(request.POST.get("weight", '0'))
        _chief_image_id = request.POST.get("chief_image", None)
        if _price:
            _price = float(_price)
        _category_id = request.POST.get("category_id", None)
        if _category_id:
            _category_id = int(_category_id)
        _entity = RBEntity(entity_id)
        _entity.update(
            category_id = _category_id,
            brand = _brand,
            title = _title,
            intro = _intro,
            price = _price,
            chief_image_id = _chief_image_id,
            weight = _weight
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def edit_entity_image(request, entity_id):
    if request.method == 'GET':
        _entity_context = RBEntity(entity_id).read()
        return render_to_response( 
            'entity/edit_image.html', 
            {
                'active_division' : 'entity',
                'entity_context' : _entity_context,
            },
            context_instance = RequestContext(request)
        )
        
@login_required
def search_entity(request):
    if request.method == 'POST':
        _query = request.POST.get("query", None)
    elif request.method == 'GET':
        _query = request.GET.get("q", None)
        
    
    _category_groups = RBCategory.allgroups()
    _entity_id_list = RBEntity.search(_query)
    _entity_context_list = [] 
    for _entity_id in _entity_id_list:
        _entity = RBEntity(_entity_id)
        _entity_context = _entity.read()
        if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
            _item_context = RBItem(_entity_context['item_id_list'][0]).read()
            _entity_context['buy_link'] = _item_context['buy_link'] 
        else:
            _entity_context['buy_link'] = ''
        _entity_context_list.append(_entity_context)
    
    _category_context_list = RBCategory.find(like_word = _query)
    
    return render_to_response( 
        'entity/search.html', 
        {
            'active_division' : 'entity',
            'query' : _query,
            'category_groups' : _category_groups,
            'entity_context_list' : _entity_context_list,
            'category_context_list' : _category_context_list,
        },
        context_instance = RequestContext(request)
    )


@login_required
def entity_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _page_num = int(request.GET.get("p", "1"))
        _category_groups = RBCategory.allgroups()
        _category_id = int(request.GET.get("cid", "1"))
        _status = request.GET.get("status", "all")
        _para = { 
            "cid" : _category_id,
            "status" : _status
        }
        if _status == "freezed":
            _status_code = -1 
        elif _status == "normal":
            _status_code = 1
        else:
            _status_code = 0
        _category_context = RBCategory(_category_id).read()
        _category_group_id = _category_context['group_id'] 
        _categories = RBCategory.find(group_id = _category_context['group_id'])
        for _category in _categories:
            _category['entity_count'] = RBEntity.count(_category['category_id'])
    
        _entity_id_list = RBEntity.find(
            category_id = _category_id,
            status = _status_code
        )
        _paginator = Paginator(_page_num, 30, len(_entity_id_list), _para)
        _entity_context_list = [] 
        for _entity_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
            _entity = RBEntity(_entity_id)
            _entity_context = _entity.read()
            if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
                _item_context = RBItem(_entity_context['item_id_list'][0]).read()
                _entity_context['buy_link'] = _item_context['buy_link'] 
            else:
                _entity_context['buy_link'] = ''
            _entity_context_list.append(_entity_context)
        
        return render_to_response( 
            'entity/list.html', 
            {
                'active_division' : 'entity',
                'status_filter' : _status, 
                'category_context' : _category_context,
                'category_groups' : _category_groups,
                'categories' : _categories,
                'category_group_id' : _category_group_id,
                'entity_context_list' : _entity_context_list,
                'paginator' : _paginator
            },
            context_instance = RequestContext(request)
        )
    else:
        _categories = RBCategory.find(group_id = int(_group_id))
        _category_groups = RBCategory.allgroups()
        if len(_categories) == 0:
            return render_to_response( 
                'entity/list.html', 
                {
                    'active_division' : 'entity',
                    'category_context' : None,
                    'category_groups' : _category_groups,
                    'categories' : _categories,
                    'category_group_id' : int(_group_id),
                    'entity_context_list' : [],
                },
                context_instance = RequestContext(request)
            )
        else:
            return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_categories[0]['category_id'])) 

@login_required
def unbind_taobao_item_from_entity(request, entity_id, item_id):
    _entity = RBEntity(entity_id)
    _entity.unbind_item(item_id)

    return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))

@login_required
def bind_taobao_item_to_entity(request, entity_id, item_id):
    _entity = RBEntity(entity_id)
    _entity.bind_item(item_id)
    return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))


@login_required
def load_taobao_item_for_entity(request, entity_id):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
            
        _entity_id = RBEntity.check_taobao_item_exist(_taobao_id)
        if _entity_id == None:
            _taobao_item_info = _load_taobao_item_info(_taobao_id)
            return render_to_response( 
                'entity/new_taobao_item_info.html', 
                {
                    'active_division' : 'entity',
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
        elif _entity_id == "":
            _item_id = RBItem.get_item_id_by_taobao_id(_taobao_id)
            _item = RBItem(_item_id)
            _item_context = _item.read()
            
            if not _item_context.has_key('images'):
                _item_context['images'] = None
            return render_to_response( 
                'entity/exist_taobao_item_info.html', 
                {
                    'active_division' : 'entity',
                    'entity_id' : entity_id,
                    'taobao_id' : _taobao_id,
                    'item_id' : _item_id,
                    'cid' : _item_context['cid'], 
                    'taobao_title' : _item_context['title'], 
                    'shop_nick' : _item_context['shop_nick'], 
                    'price' : _item_context['price'], 
                    'images' : _item_context['images'],
                    'soldout' : 0, 
                },
                context_instance = RequestContext(request)
            )
        else:
            return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity_id }) + '?code=1')
    
@login_required
def add_image_for_entity(request, entity_id):
    if request.method == "POST":
        _image_file = request.FILES.get('image', None)
        if _image_file != None:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        else:
            _image_data = None 
        _image_url= request.POST.get('image_url', None)
        _entity = RBEntity(entity_id)
        _entity.add_image(
            image_url = _image_url,
            image_data = _image_data
        )
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def del_image_from_entity(request, entity_id, image_id):
    if request.method == "GET":
        _entity = RBEntity(entity_id)
        _entity.del_image(
            image_id = image_id 
        )
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def add_taobao_item_for_entity(request, entity_id):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _taobao_soldout = request.POST.get("taobao_soldout", None)
        _image_urls = request.POST.getlist("image_url")
            
        
        _entity = RBEntity(entity_id)
        _entity.add_taobao_item(
            taobao_item_info = {
                'taobao_id' : _taobao_id,
                'cid' : _cid,
                'title' : _taobao_title,
                'shop_nick' : _taobao_shop_nick,
                'price' : _taobao_price,
                'soldout' : False,
            },
            image_urls = _image_urls
        ) 
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.get_entity_id() }))

