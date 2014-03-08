# coding=utf-8
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.template import loader
# import json

from util import *
from utils.paginator import Paginator
from base.user import User
# from base.category import Old_Category
from base.entity import Entity
# from base.note import Note
from base.models import NoteSelection
from base.tag import Tag


def search(request, template='search/search.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    _query = request.GET.get('q', None)
    _group = request.GET.get('g', 'e')  # e->entity, u->user, t->tag
    _page = request.GET.get('p', 1)

    _entity_list = []
    _user_list = []
    _tag_list = []

    _entity_id_list = Entity.search(
        query_string = _query,
    )
    _user_id_list = User.search(
        query_string = _query_string,
        offset = _offset,
        count = _count
    )
    
    
    if _group == 'e':
        _paginator = Paginator(_page, 40, len(_entity_id_list), { 'q' : _query })
        for _e_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]: 
            _entity_context = Entity(_e_id).read()
            _entity_context['is_user_already_like'] = user_already_like_entity(request.user.id, _e_id)
            _entity_list.append(_entity_context)


    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'query' : _query,
            'group' : _group,
            'entity_list' : _entity_list,
            'entity_result_count' : len(_entity_id_list),
            'user_list' : None,
            'tag_list' : None,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )
