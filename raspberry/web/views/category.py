from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.log import getLogger

from base.entity import Entity
from base.user import User 
from utils.paginator import Paginator

log = getLogger('django')

def category(request, cid, template="category/category.html"):
    if request.user.is_authenticated():
        _request_user_context = User(request.user.id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        _request_user_context = None
        _request_user_like_entity_set = []
    _page_num = request.GET.get('p', 1)
    _entity_count = Entity.count(category_id=cid, status='normal') 
    _paginator = Paginator(_page_num, 24, _entity_count)
    
    _entity_list = []
    for _entity_id in Entity.find(category_id=cid, status='normal', offset=_paginator.offset, count=_paginator.count_in_one_page):
        try:
            _entity_context = Entity(_entity_id).read()
            _entity_context['is_user_already_like'] = True if _entity_id in _request_user_like_entity_set else False
            _entity_list.append(_entity_context)
        except Exception, e:
            pass


    return render_to_response(template,
        {
            'category_id': cid,
            'entity_list' : _entity_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request))
