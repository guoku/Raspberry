#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
import HTMLParser
import re 
import datetime
import time
import json

from base.category import Category, Old_Category
from base.entity import Entity
from base.item import Item
from base.note import Note
from base.user import User
from utils.paginator import Paginator
from base import fetcher 

def _parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None

def _load_taobao_item_info(taobao_id):
    taobao_item_info = fetcher.fetch(taobao_id)
    thumb_images = []
    image_url = None
    for _img_url in taobao_item_info["imgs"]:
        thumb_images.append(_img_url)
    taobao_item_info["thumb_images"] = thumb_images
    taobao_item_info["title"] = HTMLParser.HTMLParser().unescape(taobao_item_info["desc"])
    
    taobao_item_info["shop_nick"] = taobao_item_info["nick"] 
    return taobao_item_info 

@login_required
def new_entity(request):
    if request.method == 'GET':
        _cid = int(request.GET.get("cid", "1"))
        _category_list = Category.find()
        return render_to_response(
            'entity/new.html', 
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

            _item = Item.get_item_by_taobao_id(_taobao_id)
            if _item == None:
                _taobao_item_info = _load_taobao_item_info(_taobao_id)
                _selected_category_id = int(request.POST.get("category_id", "1"))
                _brand = ''
                _title = ''
                
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
                        'category_list' : Category.find(),
                        'brand' : _brand,
                        'title' : _title,
                    },
                    context_instance = RequestContext(request)
                )
            elif _item.get_entity_id() == -1:
                #TODO: bind an exist item to entity
                pass
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
        _detail_image_urls = request.POST.getlist("image_url")
        
        if _chief_image_url in _detail_image_urls:
            _detail_image_urls.remove(_chief_image_url)
        
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
                'soldout' : False,
            },
            brand = _brand,
            title = _title,
            intro = _intro,
            detail_image_urls = _detail_image_urls,
        )

        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
def edit_entity(request, entity_id):
    if request.method == 'GET':
        _code = request.GET.get("code", None)
        if _code == "1":
            _message = "淘宝商品已被创建至本entity" 
        else:
            _message = None
        _entity_context = Entity(entity_id).read()
        _item_context_list = []
        for _item_id in _entity_context['item_id_list']:
            _item_context = Item(_item_id).read()
            if (not _entity_context.has_key('title') or _entity_context['title'] == "") and (not _entity_context.has_key('recommend_title')):
                _entity_context['recommend_title'] = _item_context['title']
            _item_context_list.append(_item_context)
        
        return render_to_response( 
            'entity/edit.html', 
            {
                'active_division' : 'entity',
                'entity_context' : _entity_context,
                'category_list' : Category.find(), 
                'old_category_list' : Old_Category.find(), 
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
        _old_category_id = request.POST.get("old_category_id", None)
        if _old_category_id:
            _old_category_id = int(_old_category_id)
        _entity = Entity(entity_id)
        _entity.update(
            category_id = _category_id,
            old_category_id = _old_category_id,
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
        _entity_context = Entity(entity_id).read()
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
        
    
    _category_groups = Category.allgroups()
#    _entity_id_list = Entity.find(like_word = _query)
    _entity_context_list = [] 
    _category_title_dict = Category.get_category_title_dict()
#    for _entity_id in _entity_id_list:
#        _entity = Entity(_entity_id)
#        _entity_context = _entity.read()
#        _entity_context['category_title'] = _category_title_dict[_entity_context['category_id']]
#        if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
#            _item_context = Item(_entity_context['item_id_list'][0]).read()
#            _entity_context['buy_link'] = _item_context['buy_link'] 
#            _entity_context['taobao_title'] = _item_context['title'] 
#        else:
#            _entity_context['buy_link'] = ''
#            _entity_context['taobao_title'] = ''
#        _entity_context_list.append(_entity_context)
    
    _category_context_list = Category.find(like_word = _query)
    
    return render_to_response( 
        'entity/search.html', 
        {
            'active_division' : 'entity',
            'query' : _query,
            'category_groups' : _category_groups,
            #'entity_context_list' : _entity_context_list,
            'entity_context_list' : [],
            'category_context_list' : _category_context_list,
        },
        context_instance = RequestContext(request)
    )


@login_required
def entity_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _status = request.GET.get("status", "all")
        if _status == "freeze":
            _status_code = -1 
        elif _status == "normal":
            _status_code = 1
        else:
            _status_code = 0
    
        _para = { 
            "status" : _status
        }
        
        _page_num = int(request.GET.get("p", "1"))
        _category_id = request.GET.get("cid", None)
        if _category_id != None:
            _category_id = int(_category_id)
            _category_context = Category(_category_id).read()
            _category_group_id = _category_context['group_id']
            _categories = Category.find(group_id = _category_context['group_id'])
            for _category in _categories:
                _category['entity_count'] = Entity.count(_category['category_id'])
            _para['cid'] = _category_id
        else:
            _category_context = None
            _category_group_id = None 
            _categories = None
        
        
        _category_groups = Category.allgroups()
        _normal_entity_count = Entity.count(category_id = _category_id, status = 0) 
        _freeze_entity_count = Entity.count(category_id = _category_id, status = -1)
        
        _entity_count = Entity.count(
            category_id = _category_id,
            status = _status_code
        )

        _paginator = Paginator(_page_num, 30, _entity_count, _para)
        _entity_id_list = Entity.find(
            category_id = _category_id,
            status = _status_code,
            offset = _paginator.offset,
            count = _paginator.count_in_one_page,
        )
        _entity_context_list = []
        _category_title_dict = Category.get_category_title_dict()
        for _entity_id in _entity_id_list:
            try:
                _entity = Entity(_entity_id)
                _entity_context = _entity.read()
                _entity_context['category_title'] = _category_title_dict[_entity_context['category_id']]
                if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
                    _item_context = Item(_entity_context['item_id_list'][0]).read()
                    _entity_context['buy_link'] = _item_context['buy_link'] 
                    _entity_context['taobao_title'] = _item_context['title'] 
                else:
                    _entity_context['buy_link'] = ''
                    _entity_context['taobao_title'] = ''
                _entity_context_list.append(_entity_context)
            except Exception, e:
                pass
        
        return render_to_response( 
            'entity/list.html', 
            {
                'active_division' : 'entity',
                'status_filter' : _status, 
                'category_context' : _category_context,
                'category_groups' : _category_groups,
                'categories' : _categories,
                'category_group_id' : _category_group_id,
                'normal_entity_count' : _normal_entity_count,
                'freeze_entity_count' : _freeze_entity_count,
                'entity_context_list' : _entity_context_list,
                'paginator' : _paginator
            },
            context_instance = RequestContext(request)
        )
    else:
        _categories = Category.find(group_id = int(_group_id))
        _category_groups = Category.allgroups()
        if len(_categories) == 0:
            _normal_entity_count = 0 
            _freeze_entity_count = 0 
            return render_to_response( 
                'entity/list.html', 
                {
                    'active_division' : 'entity',
                    'category_context' : None,
                    'category_groups' : _category_groups,
                    'categories' : _categories,
                    'category_group_id' : int(_group_id),
                    'normal_entity_count' : _normal_entity_count,
                    'freeze_entity_count' : _freeze_entity_count,
                    'entity_context_list' : [],
                },
                context_instance = RequestContext(request)
            )
        else:
            return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_categories[0]['category_id'])) 

@login_required
def unbind_taobao_item_from_entity(request, entity_id, item_id):
    _entity = Entity(entity_id)
    _entity.unbind_item(item_id)

    return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
def bind_taobao_item_to_entity(request, entity_id, item_id):
    _entity = Entity(entity_id)
    _entity.bind_item(item_id)
    return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.entity_id }))


@login_required
def load_taobao_item_for_entity(request, entity_id):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
            
        _item = Item.get_item_by_taobao_id(_taobao_id)
        if _item == None:
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
        elif _item.get_entity_id() == -1:
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
        _entity = Entity(entity_id)
        _entity.add_image(
            image_url = _image_url,
            image_data = _image_data
        )
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def del_image_from_entity(request, entity_id, image_id):
    if request.method == "GET":
        _entity = Entity(entity_id)
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
            
        
        _entity = Entity(entity_id)
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
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
def merge_entity(request, entity_id):
    if request.method == 'POST':
        _target_entity_id = request.POST.get("target_entity_id", None)
        _entity = Entity(entity_id)
        _entity.merge(_target_entity_id)
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
def get_all_categories(request):
    result = {}
    groups_and_categories = Category.all_group_with_full_category()

    for g_a_c in groups_and_categories:
        categories = []
        for cat in g_a_c['content']:
            category = {}
            category['category_title'] = cat['category_title']
            category['category_id'] = cat['category_id']
            categories.append(category)
        result[g_a_c['title']] = categories

    return HttpResponse(json.dumps(result))
