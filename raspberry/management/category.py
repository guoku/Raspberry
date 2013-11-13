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

from base.category import Category

@login_required
def create_category_group(request):
    if request.method == 'GET':
        return render_to_response( 
            'category/create_group.html', 
            {
                'active_division' : 'category',
            },
            context_instance = RequestContext(request)
        )
    else:
        _title = request.POST.get("title", None)
        _category_group_id = Category.create_group(
            title = _title
        )
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?gid=' + str(_category_group_id))

@login_required
def category_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id != None:
        _group_id = int(_group_id)
    _status = request.GET.get("status", None)
    if _status != None:
        _status = int(_status)
    _category_groups = Category.allgroups()
    _categories = Category.find(group_id = _group_id, status = _status)
    return render_to_response( 
        'category/list.html', 
        {
            'active_division' : 'category',
            'category_groups' : _category_groups,
            'categories' : _categories,
            'selected_group_id' : _group_id,
            'status' : _status
        },
        context_instance = RequestContext(request)
    )


@login_required
def create_category(request):
    if request.method == 'GET':
        _group_id = request.GET.get("gid", None)
        if _group_id != None:
            _group_id = int(_group_id)
        _category_groups = Category.allgroups()
        return render_to_response( 
            'category/create.html', 
            {
                'active_division' : 'category',
                'category_groups' : _category_groups,
                'selected_group_id' : _group_id,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _group_id = request.POST.get("group_id", None)
        _title = request.POST.get("title", None)
        _category = Category.create(
            title = _title,
            group_id = _group_id
        )
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?cid=' + str(_category.category_id)) 

@login_required
def edit_category(request, category_id):
    if request.method == 'GET':
        _category_groups = Category.allgroups()
        _category_context = Category(category_id).read()
        return render_to_response( 
            'category/edit.html', 
            {
                'active_division' : 'category',
                'category_groups' : _category_groups,
                'category_context' : _category_context,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _group_id = request.POST.get("group_id", None)
        _title = request.POST.get("title", None)
        _status = request.POST.get("status", None)
        _image_file = request.FILES.get("image_file", None)
        
        _image_data = None
        if _image_file != None:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
            
        Category(category_id).update(
            title = _title,
            group_id = _group_id,
            image_data = _image_data,
            status = _status
        )
        return HttpResponseRedirect(reverse('management.views.edit_category', kwargs = { "category_id" : category_id })) 


