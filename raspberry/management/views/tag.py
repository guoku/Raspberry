#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
from utils.authority import staff_only 
from utils.paginator import Paginator
from base.user import User
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
    _paginator = Paginator(_page_num, 30, len(_user_tag_list))

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
     
