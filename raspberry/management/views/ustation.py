#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import HTMLParser
import re 
import datetime
import time
import json

from base.entity import Entity
from base.item import Item 
from base.note import Note 
from base.taobao_shop import TaobaoShop 
from base.models import Selection, NoteSelection 
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from utils.authority import staff_only 
from utils.paginator import Paginator


def _get_ustation_entity(entity_id, update_ustation = False):
    _entity = Entity(entity_id)
    _entity_context = _entity.read()
    
    if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
        _item = Item(_entity_context['item_id_list'][0])
        _item_context = _item.read()
        
        _entity_context['buy_link'] = _item_context['buy_link'] 
        _entity_context['taobao_title'] = _item_context['title'] 
        _entity_context['taobao_id'] = _item_context['taobao_id'] 
        _entity_context['taobao_shop_nick'] = _item_context['shop_nick'] 
        
        if _item_context.has_key('shop_nick') and (not _item_context.has_key('ustation') or _item_context['ustation'] != 1):
            _shop_context = TaobaoShop(_item_context['shop_nick']).read()
            if _shop_context != None:
                _entity_context['commission_rate'] = _shop_context['extended_info']['commission_rate']
                if _shop_context['extended_info']['orientational']:
                    _entity_context['commission_type'] = 'orientational'
                else:
                    _entity_context['commission_type'] = 'general'
                if _entity_context['commission_rate'] > 0:
                    if update_ustation:
                        if not _item_context.has_key('ustation') or _item_context['ustation'] == None:
                            _item.update(ustation = 0)
                    return _entity_context
    return None



def _available_ustation_list():
    
    _t_top = datetime.datetime.now()
    _t_bottom = datetime.datetime.now() - datetime.timedelta(hours = 48)

    _entity_context_list = []
    _entity_id_set = set() 
    for _item_info in Item.find_ustation():
        _entity_context = _get_ustation_entity(_item_info['entity_id'])
        if _entity_context != None:
            _entity_context_list.append(_entity_context)
            _entity_id_set.add(_item_info['entity_id'])
            
    for _selection in NoteSelection.objects.filter(post_time__lt =  _t_top, post_time__gt = _t_bottom).order_by('-post_time'):
        try:
            if not _selection.entity_id in _entity_id_set:
                _entity_context = _get_ustation_entity(_selection.entity_id, True)
                if _entity_context != None:
                    _entity_context_list.append(_entity_context)
                    _entity_id_set.add(_selection.entity_id)
        except Exception, e:
            pass

    return _entity_context_list


@login_required
@staff_only
def ustation_list(request):
    _entity_context_list = _available_ustation_list() 
    return render_to_response( 
        'ustation/list.html', 
        {
            'active_division' : 'ustation',
            'entity_context_list' : _entity_context_list,
        },
        context_instance = RequestContext(request)
    )

#@login_required
#@staff_only
def sync_ustation(request):
    _entity_context_list = _available_ustation_list() 
    _rslt = []
    for _entity_context in _entity_context_list:
        try:
            _note_id = Note.find(entity_id = _entity_context['entity_id'], selection = 1)[0]
            _note_context = Note(_note_id).read()
            _rslt.append({
                'item_id' : _entity_context['taobao_id'],
                'cid' : _entity_context['old_root_category_id'],
                'note' : _note_context['content']
            })
        except Exception, e:
            pass

    return SuccessJsonResponse(_rslt)

@login_required
@staff_only
def clean_ustation(request):
    for _item_info in Item.find_ustation():
        _item = Item(_item_info['item_id'])
        _item.update(ustation = 1)
    
    return HttpResponseRedirect(reverse('management_ustation_list'))
    

@login_required
@staff_only
def ustation_random_generate(request):
    if request.method == "GET":
        return render_to_response( 
            'ustation/random.html', 
            {
                'active_division' : 'ustation',
            },
            context_instance = RequestContext(request)
        )
    else:
        _count = int(request.POST.get("count", None))
        _entity_id_list = Entity.random(status = 'select', count = _count * 6)
        _entity_context_list = []
        for _entity_id in _entity_id_list:
            try:
                _entity_context = _get_ustation_entity(_entity_id, True)
                if _entity_context != None:
                    _entity_context_list.append(_entity_context)
                    if len(_entity_context_list) >= _count:
                        break
            except Exception, e:
                pass
        
        return HttpResponseRedirect(reverse('management_ustation_list'))
         
