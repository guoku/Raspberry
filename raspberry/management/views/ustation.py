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
from base.taobao_shop import TaobaoShop 
from base.models import Selection, NoteSelection 
from utils.authority import staff_only 
from utils.paginator import Paginator


def _get_ustation_new_selection_list():
    _t_top = datetime.datetime.now()
    _t_bottom = datetime.datetime.now() - datetime.timedelta(hours = 480)

    _entity_context_list = []
    for _selection in NoteSelection.objects.filter(post_time__lt =  _t_top, post_time__gt = _t_bottom).order_by('-post_time'):
        _entity_id = _selection.entity_id
        _entity = Entity(_entity_id)
        _entity_context = _entity.read()
        
        if _entity_context.has_key('item_id_list') and len(_entity_context['item_id_list']):
            _item_context = Item(_entity_context['item_id_list'][0]).read()
            _entity_context['buy_link'] = _item_context['buy_link'] 
            _entity_context['taobao_title'] = _item_context['title'] 
            _entity_context['taobao_id'] = _item_context['taobao_id'] 
            _entity_context['taobao_shop_nick'] = _item_context['shop_nick'] 
            
            if _item_context.has_key('shop_nick'):
                _shop_context = TaobaoShop(_item_context['shop_nick']).read()
                print _shop_context
                if _shop_context != None:
                    _entity_context['commission_rate'] = _shop_context['commission_rate']
                    _entity_context['commission_type'] = _shop_context['commission_type']
                    if _entity_context['commission_rate'] > 0:
                        _entity_context_list.append(_entity_context)
    
    return _entity_context_list



@login_required
@staff_only
def ustation_list(request):
    _entity_context_list = _get_ustation_new_selection_list()
    return render_to_response( 
        'ustation/pending.html', 
        {
            'active_division' : 'ustation',
            'entity_context_list' : _entity_context_list,
        },
        context_instance = RequestContext(request)
    )
    

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
        _entity_id_list = Entity.random()
         
