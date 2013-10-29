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

from common.category import RBCategory
from common.entity import RBEntity
from common.item import RBItem


@login_required
def note_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _category_groups = RBCategory.allgroups()
        _category_id = int(request.GET.get("cid", "1"))
        _category_context = RBCategory(_category_id).read()
        _category_group_id = _category_context['group_id'] 
        _categories = RBCategory.find(group_id = _category_context['group_id'])
        for _category in _categories:
            _category['entity_count'] = RBEntity.count(_category['category_id'])
    
        _entity_id_list = RBEntity.find(_category_id)
        _entity_context_list = [] 
        for _entity_id in _entity_id_list:
            _entity_context_list.append(RBEntity(_entity_id).read())
        
        return render_to_response( 
            'entity/list.html', 
            {
                'active_division' : 'entity',
                'category_context' : _category_context,
                'category_groups' : _category_groups,
                'categories' : _categories,
                'category_group_id' : _category_group_id,
                'entity_context_list' : _entity_context_list,
            },
            context_instance = RequestContext(request)
        )
    else:
        _categories = RBCategory.find(group_id = int(_group_id))
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_categories[0]['category_id'])) 

            )
        else:
            return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity_id }) + '?code=1')
    
