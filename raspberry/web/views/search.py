# coding=utf-8
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.user import User
from base.entity import Entity
from base.models import NoteSelection
from base.tag import Tag
from utils.paginator import Paginator
from utils.lib import get_client_ip
from web.tasks import WebLogTask
import datetime


def search(request, template='search/search.html'):
    # _start_at = datetime.datetime.now()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_context = User(_request_user_id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        # _request_user_id = None
        _request_user_context = None
        _request_user_like_entity_set = [] 

    _query = request.GET.get('q', None)
    _group = request.GET.get('g', 'e')  # e->entity, u->user, t->tag
    _page = request.GET.get('p', 1)

    _entity_list = []
    _user_list = []
    _tag_list = []
    _log_appendix = { 'query' : _query }
   
    if _query == None or _query == '':
        _entity_id_list = []
        _user_id_list = []
        _tag_list = []
        _paginator = None
    else:
        _entity_id_list = Entity.search(
            query_string=_query,
        )
        _user_id_list = User.search(
            query_string=_query,
        )
        _tag_list = Tag.search(
            query_string=_query
        )
        
        
        if _group == 'u':
            _paginator = Paginator(_page, 8, len(_user_id_list), { 'q' : _query, 'g' : 'u' })
            for _u_id in _user_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]: 
                try:
                    _user = User(_u_id)
                    _user_context = _user.read()
                    if _request_user_context != None:
                        _user_context['relation'] = User.get_relation(_request_user_context['user_id'], _u_id)
                    _user_context['latest_like_entity_id_list'] = _user.read_latest_like_entity_list() 
                    _user_list.append(_user_context)
                except Exception, e:
                    pass
            _log_appendix['type'] = 'user'
            _log_appendix['result_users'] = _user_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]
        elif _group == 't':
            _paginator = Paginator(_page, 24, len(_tag_list), { 'q' : _query, 'g' : 't' })
            _log_appendix['type'] = 'tag'
            _log_appendix['result_tags'] = [] 
            for _tag_context in _tag_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
                try:
                    _tag_entity_id_list = Tag.find_tag_entity(_tag_context['tag_hash'])
                    _tag_context['entity_count'] = len(_tag_entity_id_list)
                    _tag_context['entity_list'] = [Entity(x).read() for x in _tag_entity_id_list[:4]]
                    _log_appendix['result_tags'].append(_tag_context['tag'])
                except Exception, e:
                    pass
        else:
            _paginator = Paginator(_page, 24, len(_entity_id_list), { 'q' : _query })
            _log_appendix['type'] = 'entity'
            _log_appendix['result_entities'] = _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]
            for _e_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
                try:
                    _entity_context = Entity(_e_id).read()
                    _entity_context['is_user_already_like'] = True if _e_id in _request_user_like_entity_set else False
                    _entity_list.append(_entity_context)
                except Exception, e:
                    pass

    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='SEARCH',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix=_log_appendix
    # )
    
    return render_to_response(
        template,
        {
            'user_context' : _request_user_context,
            'query' : _query,
            'group' : _group,
            'entity_list' : _entity_list,
            'entity_result_count' : len(_entity_id_list),
            'user_list' : _user_list,
            'user_result_count' : len(_user_id_list),
            'tag_list' : _tag_list,
            'tag_result_count' : len(_tag_list),
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )
