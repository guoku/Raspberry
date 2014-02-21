#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
from utils.authority import staff_only 
from utils.paginator import Paginator
from base.category import Category, Old_Category
from base.entity import Entity
from base.note import Note
from base.item import Item
from base.user import User
from base.taobao_shop import TaobaoShop 
from base.tag import Tag 
import HTMLParser
import re 
import datetime
import time
import json


@login_required
@staff_only
def user_tag_list(request):
    _page_num = int(request.GET.get("p", "1"))
    _type = request.GET.get("type", "all")
    _user_id = request.GET.get("user", None)
    if _user_id != None:
        _user_id = int(_user_id)
    _tag = request.GET.get("tag", None)

    _recommend_user_tag_list = Tag.get_recommend_user_tag_list(with_entity_count = False)
    
    if _type == 'recommend':
        _user_tag_list = []
        for _user_tag in _recommend_user_tag_list:
            _user_tag_list.append({
                'user_id' : _user_tag[0], 
                'tag_text' : _user_tag[1], 
                'entity_count' : Tag.get_user_tag_entity_count(_user_tag[0], _user_tag[1])
            })
    else:
        _user_tag_list = Tag.find_user_tag(user_id = _user_id, tag = _tag)
    _paginator = Paginator(_page_num, 30, len(_user_tag_list), {"type" : _type})

    _context_list = []
    for _data in _user_tag_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _user = User(_data['user_id'])
            _user_context = _user.read()
            if [_user_context['user_id'], _data['tag_text']] in _recommend_user_tag_list:
                _status = 1
            else:
                _status = 0
            _context_list.append({
                'tag' : _data['tag_text'],
                'user' : _user_context, 
                'entity_count' : _data['entity_count'],
                'status' : _status
            })
        except Exception, e:
            pass

    return render_to_response( 
        'tag/list.html', 
        {
            'active_division' : 'tag',
            'type' : _type,
            'context_list' : _context_list,
            'paginator' : _paginator,
        },
        context_instance = RequestContext(request)
    )

@login_required
@staff_only
def user_tag_entity_list(request, user_id, tag):
    _page_num = int(request.GET.get("p", "1"))
    _entity_id_list = Tag.find_user_tag_entity(user_id, tag)
    _paginator = Paginator(_page_num, 30, len(_entity_id_list))
    _category_title_dict = Category.get_category_title_dict()
    _user_context = User(user_id).read()
    
    _entity_context_list = []
    for _entity_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
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
                        if _shop_context['extended_info']['commission'] == True:
                            _entity_context['commission_rate'] = _shop_context['extended_info']['commission_rate']
                            if _shop_context['extended_info']['orientational']:
                                _entity_context['commission_type'] = 'orientational'
                            else:
                                _entity_context['commission_type'] = 'general'
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
        'tag/entity_list.html', 
        {
            'active_division' : 'tag',
            'tag' : tag,
            'entity_context_list' : _entity_context_list,
            'user_context' : _user_context,
            'paginator' : _paginator,
        },
        context_instance = RequestContext(request)
    )
        


@login_required
@staff_only
def transcend_user_tag(request, tag, user_id):
    Tag.add_recommend_user_tag(
        user_id = user_id,
        tag = tag,
    ) 
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
     
@login_required
@staff_only
def freeze_user_tag(request, tag, user_id):
    Tag.del_recommend_user_tag(
        user_id = user_id,
        tag = tag,
    ) 
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
     
