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
from base.entity import Entity

from base.category import Category, Category_Group

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
        _category_group = Category_Group.create(
            title = _title
        )
        return HttpResponseRedirect(reverse('management.views.entity_list') + '?gid=' + str(_category_group.category_group_id))

@login_required
def edit_category_group(request, category_group_id):
    if request.method == 'GET':
        _category_group_context = Category_Group(category_group_id).read()
        return render_to_response( 
            'category/edit_group.html', 
            {
                'active_division' : 'category',
                'category_group_context' : _category_group_context,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _title = request.POST.get("title", None)
        _status = request.POST.get("status", None)
        
        Category_Group(category_group_id).update(
            title = _title,
            status = _status
        )
        return HttpResponseRedirect(reverse('management.views.category_list') + '?gid=' + str(category_group_id)) 



@login_required
def category_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id != None:
        _group_id = int(_group_id)
    _status = request.GET.get("status", None)
    if _status != None:
        _status = int(_status)

    _all_count = len(Category.find(group_id=_group_id))
    _normal_count = len(Category.find(group_id=_group_id, status=1))
    _freeze_count = _all_count - _normal_count

    _category_groups = Category.allgroups()
    _categories = Category.find(group_id = _group_id, status = _status, order_by = '-status')

    for _category in _categories:
        _category["group_title"] = Category_Group(_category["group_id"]).read()["title"]

    return render_to_response( 
        'category/list.html', 
        {
            'active_division' : 'category',
            'category_groups' : _category_groups,
            'categories' : _categories,
            'selected_group_id' : _group_id,
            'status' : _status,
            'all_count' : _all_count,
            'normal_count' : _normal_count,
            'freeze_count' : _freeze_count
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
        _category_entity_count = Entity.count(category_id)
        return render_to_response( 
            'category/edit.html', 
            {
                'active_division' : 'category',
                'category_groups' : _category_groups,
                'category_context' : _category_context,
                'category_entity_count' : _category_entity_count
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

