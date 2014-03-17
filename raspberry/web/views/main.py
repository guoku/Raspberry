# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.utils.log import getLogger
# import json
from utils.http import JSONResponse
from datetime import datetime

from utils.paginator import Paginator
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.tag import Tag 
from base.user import User
from base.category import Old_Category
import base.popularity as popularity

from web.tasks import WebLogTask
from utils.lib import get_client_ip

log = getLogger('django')

def index(request):
    return HttpResponseRedirect(reverse('web_selection'))

@require_http_methods(['GET'])
def selection(request, template='main/selection.html'):
    _start_at = datetime.now()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_context = User(_request_user_id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        _request_user_id = None 
        _request_user_context = None
        _request_user_like_entity_set = [] 
     
    _old_category_list = Old_Category.find()[0:11]

    _page_num = int(request.GET.get('p', 1))
    _category_id = request.GET.get('c', None)
    
    _hdl = NoteSelection.objects.filter(post_time__lt = datetime.now())
    if _category_id != None:
        _category_id = int(_category_id)
        _hdl = _hdl.filter(root_category_id=_category_id)
    else:
        _category_id = 0
    _hdl.order_by('-post_time')
    
    _paginator = Paginator(_page_num, 30, _hdl.count())
    _note_selection_list = _hdl[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]

    _selection_list = []
    _entity_id_list = []
    for _note_selection in _note_selection_list:
        try:
            _selection_note_id = _note_selection['note_id']
            _entity_id = _note_selection['entity_id']
            _entity_context = Entity(_entity_id).read()
    
            _note = Note(_selection_note_id)
            _note_context = _note.read()
            _creator_context = User(_note_context['creator_id']).read()
            _is_user_already_like = True if _entity_id in _request_user_like_entity_set else False
            
            _selection_list.append(
                {
                    'is_user_already_like': _is_user_already_like,
                    'entity_context': _entity_context,
                    'note_context': _note_context,
                    'creator_context': _creator_context,
                }
            )
            _entity_id_list.append(_entity_id)
        except Exception, e:
            pass

    _duration = datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds, 
        page='SELECTION', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'root_category_id' : int(_category_id),
            'result_entities' : _entity_id_list,
        },
    )
    # 判断是否第一次加载
    if _page_num == 1:
        return render_to_response(
            template,
            {
                'main_nav_deliver' : 'selection',
                'page_num' : _page_num,
                'curr_category_id' : _category_id,
                'user_context' : _request_user_context,
                'category_list' : _old_category_list,
                'selection_list' : _selection_list,
            },
            context_instance = RequestContext(request)
        )

    else:
        _ret = {
            'status' : 0,
            'msg' : '没有更多数据'
        }

        if _selection_list:
            _t = loader.get_template('main/partial/selection_item_list.html')
            _c = RequestContext(request, {
                'selection_list': _selection_list,
            })
            _data = _t.render(_c)

            _ret = {
                'status' : '1',
                'data' : _data
            }
        return JSONResponse(data=_ret)

def wap_selection(request, template='wap/selection.html'):
    _agent = 'iphone'
    if 'Android' in request.META['HTTP_USER_AGENT']:
        _agent = 'android'
   
    _page_num = int(request.GET.get('p', 1))
    _hdl = NoteSelection.objects.filter(post_time__lt = datetime.now())
    _paginator = Paginator(_page_num, 30, _hdl.count())
    _hdl = _hdl.order_by('-post_time')
    _selection_list = []
    for _note_selection in _hdl[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        _selection_note_id = _note_selection['note_id']
        _entity_id = _note_selection['entity_id']
        _entity_context = Entity(_entity_id).read()
        _note_context = Note(_selection_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()
        
        _selection_list.append({
            'entity_context': _entity_context,
            'note_context': _note_context,
            'creator_context': _creator_context,
        })
        
    return render_to_response(
        template,
        {
            'agent' : _agent,
            'selection_list' : _selection_list,
            'next_page_num' : _page_num + 1,
        },
        context_instance=RequestContext(request)
    )




@require_http_methods(['GET'])
def popular(request, template='main/popular.html'):
    if request.user.is_authenticated():
        _request_user_context = User(request.user.id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        _request_user_context = None
        _request_user_like_entity_set = [] 
    
    _group = request.GET.get('group', 'daily')
    _popular_list = []
    _popular_updated_time = datetime.now() 
   
    _popular_entities = popularity.read_popular_entity_from_cache(scale=_group)
    if _popular_entities != None:
        _popular_updated_time = _popular_entities['updated_time']
        for row in _popular_entities['data'][0:60]:
            try:
                _entity_id = row[0]
                _entity = Entity(_entity_id)
                _entity_context = _entity.read()
                _is_user_already_like = True if _entity_id in _request_user_like_entity_set else False
        
                _popular_list.append({
                    'is_user_already_like' : _is_user_already_like,
                    'entity_context' : _entity_context,
                })
            except Exception, e:
                pass

    return render_to_response(
        template,
        {
            'group' : _group,
            'user_context' : _request_user_context,
            'popular_updated_time' : _popular_updated_time, 
            'popular_list' : _popular_list
        },
        context_instance=RequestContext(request)
    )

