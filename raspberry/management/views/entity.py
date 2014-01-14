#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
import HTMLParser
import re 
import datetime
import time
import json
from base import fetcher 
from base.category import Category, Old_Category
from base.entity import Entity
from base.item import Item
from base.note import Note
from base.taobao_shop import TaobaoShop 
from base.user import User
from management.tasks import CreateTaobaoShopTask
from utils.authority import staff_only 
from utils.paginator import Paginator

def _parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None

def _load_taobao_item_info(taobao_id):
    taobao_item_info = fetcher.fetch_item(taobao_id)
    thumb_images = []
    image_url = None
    for _img_url in taobao_item_info["imgs"]:
        thumb_images.append(_img_url)
    taobao_item_info["thumb_images"] = thumb_images
    taobao_item_info["title"] = HTMLParser.HTMLParser().unescape(taobao_item_info["desc"])
    
    taobao_item_info["shop_nick"] = taobao_item_info["nick"]
    
    return taobao_item_info


def _get_special_names(request_user_id):
    if request_user_id in [22045, 19, 10, 79761, 66400, 195580]:
        if request_user_id == 22045:
            _id_list = [ 22045, 149556, 14, 149308, 195580, 68310, 209071, 105, 173660, 95424, 215653, 218336, 216902]
        elif request_user_id in [10, 19]:
            _id_list = [ 19, 10, 22045, 149556, 14, 149308, 195580, 68310, 209071, 105, 173660, 95424, 215653, 218336, 216902]
        elif request_user_id == 195580:
            _id_list = [ 195580, 215653, 209071 ] 
        elif request_user_id in [79761, 66400]:
            _id_list = [ 66400, 79761 ]
            

        _users = []
        for _id in _id_list:
            _user_context = User(_id).read()
            _users.append({
                'id' : _id,
                'name' : _user_context['nickname']
            })
    else:
        _request_user_context = User(request_user_id).read()
        _users = [
            {
                'name': _request_user_context['nickname'],
                'id': str(request_user_id)
            }
        ]
    return _users


def _add_note_and_select_delay(entity, user_id, note):
    if len(note.strip()) > 0:
        _note = entity.add_note(creator_id=user_id, note_text=note)

        if user_id in ['22045', '149556', '14', '149308', '195580', '68310', '209071', '105', '173660',
                       '95424', '215653', '218336', '216902', '19', '10', '79761', '66400']:
            Entity(entity.read()['entity_id']).update_note_selection_info(
                note_id=_note.read()['note_id'],
                selector_id=user_id,
                selected_time=datetime.datetime.now(),
                post_time=datetime.datetime(2100, 1, 1)
            )


@login_required
@staff_only
def new_entity(request):
    if request.method == 'GET':
        return render_to_response(
            'entity/new.html',
            {
                'active_division': 'entity'
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
                _brand = ''
                _title = ''
                _selected_category_id = Category.get_category_by_taobao_cid(_taobao_item_info['cid'])

                _users = _get_special_names(request.user.id)

                return render_to_response(
                    'entity/create.html', 
                    {
                        'active_division': 'entity',
                        'taobao_id': _taobao_id,
                        'cid': _taobao_item_info['cid'],
                        'taobao_title': _taobao_item_info['title'],
                        'shop_nick': _taobao_item_info['shop_nick'],
                        'shop_link': _taobao_item_info['shop_link'],
                        'price': _taobao_item_info['price'],
                        'thumb_images': _taobao_item_info["thumb_images"],
                        'selected_category_id': _selected_category_id,
                        'category_list': Category.find(),
                        'brand': _brand,
                        'title': _title,
                        'users': _users
                    },
                    context_instance=RequestContext(request)
                )
            elif _item.get_entity_id() == -1:
                #TODO: bind an exist item to entity
                pass
            else:
                return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _item.get_entity_id() }) + '?code=1')
                
                
@login_required
@staff_only
def create_entity_by_taobao_item(request):
    if request.method == 'POST':
        _taobao_id = request.POST.get("taobao_id", None)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("taobao_shop_nick", None)
        _taobao_shop_link = request.POST.get("taobao_shop_link", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = request.POST.get("taobao_price", None)
        _chief_image_url = request.POST.get("chief_image_url", None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = ""
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

        _note = request.POST.get("note", None)
        _user_id = request.POST.get("user_id", None)
        
        if _note != None and len(_note) > 0:
            _add_note_and_select_delay(_entity, _user_id, _note)

        CreateTaobaoShopTask.delay(_taobao_shop_nick, _taobao_shop_link)

        return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
@staff_only
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
            _item_context['commission_type'] = 'unknown' 
            _item_context['commission_rate'] = -1 
            if _item_context.has_key('shop_nick'):
                _shop_context = TaobaoShop(_item_context['shop_nick']).read()
                if _shop_context != None:
                    _item_context['commission_rate'] = _shop_context['commission_rate']
                    _item_context['commission_type'] = _shop_context['commission_type']
            _item_context_list.append(_item_context)


        _note_count = Note.count(entity_id=entity_id)

        _users = _get_special_names(request.user.id)
        _mark_list = Entity.Mark.all()

        return render_to_response( 
            'entity/edit.html', 
            {
                'active_division' : 'entity',
                'entity_context' : _entity_context,
                'category_list' : Category.find(), 
                'old_category_list' : Old_Category.find(), 
                'item_context_list' : _item_context_list,
                'mark_list' : _mark_list,
                'message' : _message,
                'note_count': _note_count,
                'users' : _users
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _intro = request.POST.get("intro", None)
        _price = request.POST.get("price", None)
        _weight = int(request.POST.get("weight", '0'))
        _mark = int(request.POST.get("mark", '0'))
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
            weight = _weight,
            mark = _mark
        )

        _note = request.POST.get("note", None)
        _user_id = request.POST.get("user_id", None)
        if _note != None and len(_note) > 0:
            _add_note_and_select_delay(_entity, _user_id, _note)

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@staff_only
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
@staff_only
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
@staff_only
def entity_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _status = request.GET.get("status", "select")
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
        _select_entity_count = Entity.count(category_id = _category_id, status = 'select') 
        _novus_entity_count = Entity.count(category_id = _category_id, status = 'novus') 
        _freeze_entity_count = Entity.count(category_id = _category_id, status = 'freeze')
        _recycle_entity_count = Entity.count(category_id = _category_id, status = 'recycle')
        
        _sort_by = request.GET.get("sort_by", "updated")
        _reverse = request.GET.get("reverse", None)
        if _sort_by:
            _para["sort_by"] = _sort_by
            _para["reverse"] = _reverse
            if _reverse == '1':
                _reverse = True
            else:
                _reverse = False
        
        _entity_count = Entity.count(
            category_id = _category_id,
            status = _status
        )
    
        if _sort_by == 'random':
            _paginator = None
            _entity_id_list = Entity.random(
                status = _status,
                count = 30
            )
        else:
            _paginator = Paginator(_page_num, 30, _entity_count, _para)

            _entity_id_list = Entity.find(
                category_id = _category_id,
                status = _status,
                offset = _paginator.offset,
                count = _paginator.count_in_one_page,
                sort_by = _sort_by,
                reverse = _reverse
            )
        
        _entity_context_list = []
        _category_title_dict = Category.get_category_title_dict()
        for _entity_id in _entity_id_list:
            try:
                _entity = Entity(_entity_id)
                _entity_context = _entity.read()
                _entity_context['category_title'] = _category_title_dict[_entity_context['category_id']]
                _entity_context['commission_rate'] = -1 
                _entity_context['commission_type'] = 'unknown' 
                if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
                    _item_context = Item(_entity_context['item_id_list'][0]).read()
                    _entity_context['buy_link'] = _item_context['buy_link'] 
                    _entity_context['taobao_title'] = _item_context['title'] 
                    _entity_context['taobao_id'] = _item_context['taobao_id'] 
                    _entity_context['taobao_shop_nick'] = _item_context['shop_nick'] 
                    
                    if _item_context.has_key('shop_nick'):
                        _shop_context = TaobaoShop(_item_context['shop_nick']).read()
                        if _shop_context != None:
                            _entity_context['commission_rate'] = _shop_context['commission_rate']
                            _entity_context['commission_type'] = _shop_context['commission_type']
                else:
                    _entity_context['buy_link'] = ''
                    _entity_context['taobao_title'] = ''
                    _entity_context['taobao_id'] = ''
                _entity_context['is_selected'] = False
                if _entity_context.has_key('note_id_list') and len(_entity_context['note_id_list']):
                    for _note_id in _entity_context['note_id_list']:
                        _note_context = Note(_note_id).read()
                        if _note_context['is_selected']:
                            _entity_context['is_selected'] = True
                            break
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
                'select_entity_count' : _select_entity_count,
                'novus_entity_count' : _novus_entity_count,
                'freeze_entity_count' : _freeze_entity_count,
                'recycle_entity_count' : _recycle_entity_count,
                'entity_context_list' : _entity_context_list,
                'paginator' : _paginator,
                'sort_by' : _sort_by,
                'reverse' : _reverse
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
            return HttpResponseRedirect(reverse('management_entity_list') + '?cid=' + str(_categories[0]['category_id'])) 

@login_required
@staff_only
def unbind_taobao_item_from_entity(request, entity_id, item_id):
    _entity = Entity(entity_id)
    _entity.unbind_item(item_id)

    return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
@staff_only
def bind_taobao_item_to_entity(request, entity_id, item_id):
    _entity = Entity(entity_id)
    _entity.bind_item(item_id)
    return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity.entity_id }))


@login_required
@staff_only
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
            return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity_id }) + '?code=1')
    
@login_required
@staff_only
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
@staff_only
def del_image_from_entity(request, entity_id, image_id):
    if request.method == "GET":
        _entity = Entity(entity_id)
        _entity.del_image(
            image_id = image_id 
        )
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@staff_only
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
        return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
@staff_only
def merge_entity(request, entity_id):
    if request.method == 'POST':
        _target_entity_id = request.POST.get("target_entity_id", None)
        _entity = Entity(entity_id)
        _entity.merge(_target_entity_id)
        return HttpResponseRedirect(reverse('management_edit_entity', kwargs = { "entity_id" : _entity.entity_id }))

@login_required
@staff_only
def get_all_categories(request):
    if request.method == 'GET':
        result = {}
        new_category = {}
        result['new_category'] = new_category
        result['old_category'] = Old_Category.find()
        groups_and_categories = Category.all_group_with_full_category()

        for g_a_c in groups_and_categories:
            categories = []

            for cat in g_a_c['content']:
                category = {
                    'category_title' : cat['category_title'],
                    'category_id' : cat['category_id']
                }
                categories.append(category)

            new_category[g_a_c['title']] = categories

        return HttpResponse(json.dumps(result))

@login_required
@staff_only
def read_taobao_item_state(request):
    _taobao_url = request.GET.get("url", None)
    _item = None
    if _taobao_url is not None:
        _taobao_id = _parse_taobao_id_from_url(_taobao_url)
        _item = Item.get_item_by_taobao_id(_taobao_id)

    _result = {}

    if _item is None:
        _result['status'] = 0
    elif _item.get_entity_id() == -1:
        _result['status'] = -1
    else:
        _result['status'] = 1
        _entity_id = _item.get_entity_id()
        _entity = Entity(_entity_id).read()
        _result['entity'] = _entity

    return HttpResponse(json.dumps(_result, cls=DjangoJSONEncoder))

@login_required
@staff_only
def recycle_entity(request, entity_id):
    if request.method == 'POST':
        _entity = Entity(entity_id)
        _entity.update(
            weight = -2
        )
        return HttpResponse(1)
