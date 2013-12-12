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

from base.user import User
from utils.paginator import Paginator


@login_required
def user_list(request):
    _page_num = int(request.GET.get("p", "1"))
    _user_count = User.count()
    _paginator = Paginator(_page_num, 30, _user_count)
    _user_id_list = User.find(
        offset = _paginator.offset,
        count = _paginator.count_in_one_page,
    )
        
    _context_list = []
    for _user_id in _user_id_list:
        try:
            _user = User(_user_id)
            _user_context = _user.read()
            _context_list.append(_user_context)
        except Exception, e:
            pass
        
    return render_to_response( 
        'user/list.html', 
        {
            'active_division' : 'user',
            'context_list' : _context_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )


@login_required
def edit_user(request, user_id):
    if request.method == 'GET':
        _user_context = User(user_id).read()
        return render_to_response( 
            'user/edit.html', 
            {
                'active_division' : 'user',
                'user_context' : _user_context,
            },
            context_instance = RequestContext(request)
        )




