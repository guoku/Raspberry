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
    _user_tag_list = Tag.find_user_tag() 
    _paginator = Paginator(_page_num, 30, len(_user_tag_list))
        
        
    _context_list = []
    for _data in _user_tag_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _user = User(_data['user_id'])
            _user_context = _user.read()
            _context_list.append({
                'tag' : _data['tag_text'],
                'user' : _user_context, 
                'entity_count' : _data['entity_count'],
            })
        except Exception, e:
            print e
            pass

    return render_to_response( 
        'tag/list.html', 
        {
            'active_division' : 'tag',
            'context_list' : _context_list,
            'paginator' : _paginator,
        },
        context_instance = RequestContext(request)
    )


