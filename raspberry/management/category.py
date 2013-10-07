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

@login_required
def create_category(request):
    if request.method == 'GET':
        _group_id = request.GET.get("gid", None)
        if _group_id != None:
            _group_id = int(_group_id)
        _category_groups = RBCategory.allgroups()
        return render_to_response( 
            'category/create.html', 
            {
              'category_groups' : _category_groups,
              'selected_group_id' : _group_id,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _group_id = request.POST.get("group_id", None)
        _title = request.POST.get("title", None)
        _category = RBCategory.create(
            title = _title,
            group_id = _group_id
        )
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_category.get_category_id())) 

@login_required
def edit_category(request, category_id):
    if request.method == 'GET':
        _category_groups = RBCategory.allgroups()
        _category_context = RBCategory(category_id).read()
        return render_to_response( 
            'category/edit.html', 
            {
              'category_groups' : _category_groups,
              'category_context' : _category_context,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _group_id = request.POST.get("group_id", None)
        _title = request.POST.get("title", None)
        RBCategory(category_id).update(
            title = _title,
            group_id = _group_id
        )
        return HttpResponseRedirect(reverse('management.views.edit_category', kwargs = { "category_id" : category_id })) 

