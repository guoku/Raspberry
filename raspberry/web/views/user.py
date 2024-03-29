# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.log import getLogger

from base.user import User
from base.category import Old_Category
from base.entity import Entity
from base.note import Note
from base.models import NoteSelection
from base.tag import Tag
from utils.lib import get_client_ip
from utils.paginator import Paginator
from web.tasks import WebLogTask
import datetime 


TEMPLATE = 'user/index.html'
log = getLogger('django')

def user_index(request, user_id):
    return HttpResponseRedirect(reverse('web_user_likes', args=[user_id]))


def user_likes(request, user_id, template=TEMPLATE):
    _start_at = datetime.datetime.now()
    _category_id = request.GET.get('c', None)
    _page_num = int(request.GET.get('p', '1'))
    _price = request.GET.get('price', None)
    _query_user = User(user_id)
    _query_user_context = _query_user.read() 
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _is_staff = request.user.is_staff
        _request_user_context = User(_request_user_id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
        _relation = User.get_relation(_request_user_context['user_id'], _query_user_context['user_id']) 
    else:
        _request_user_id = None
        _is_staff = False 
        _request_user_context = None
        _request_user_like_entity_set = []
        _relation = None 
    
    _old_category_list = Old_Category.find()[0:12]
    _param = {}
    if _category_id is not None:
        _category_id = int(_category_id)
        _param['c'] = _category_id
    
    _paginator = Paginator(_page_num, 24, _query_user.entity_like_count(category_id=_category_id), _param)
    _entity_id_list = _query_user.find_like_entity(_category_id, offset=_paginator.offset, count=_paginator.count_in_one_page)
    _entity_list = []
    for _e_id in _entity_id_list:
        try:
            _entity_context = Entity(_e_id).read()
            _entity_context['is_user_already_like'] = True if _e_id in _request_user_like_entity_set else False
            _entity_list.append(_entity_context)
        except Exception, e:
            pass
    
    _duration = datetime.datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds, 
        page='USER_LIKE', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'user_id' : int(user_id),
            'result_entities' : _entity_id_list,
        },
    )

    return render_to_response(
        template,
        {
            'is_staff' : _is_staff,
            'content_tab' : 'like',
            'request_user_context' : _request_user_context,
            'query_user_context' : _query_user_context,
            'relation' : _relation,
            'category_list' : _old_category_list,
            'category_id' : _category_id,
            'price' : _price,
            'entity_list' : _entity_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_notes(request, user_id, template=TEMPLATE):
    _start_at = datetime.datetime.now()
    _query_user = User(user_id)
    _query_user_context = _query_user.read() 
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_context = User(_request_user_id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
        _relation = User.get_relation(_request_user_context['user_id'], _query_user_context['user_id']) 
    else:
        _request_user_id = None 
        _request_user_context = None
        _request_user_like_entity_set = []
        _relation = None 
    

    _page_num = int(request.GET.get('p', 1))
    _paginator = Paginator(_page_num, 24, Note.count(creator_set=[user_id]))
    _note_id_list = Note.find(creator_set=[user_id], offset=_paginator.offset, count=_paginator.count_in_one_page)
    _note_list = []
    for _n_id in _note_id_list:
        try:
            _note_context = Note(_n_id).read()
            _entity_id = _note_context['entity_id']
            _creator_context = User(user_id).read()
            _entity_context = Entity(_entity_id).read()
            _is_user_already_like = True if _entity_id in _request_user_like_entity_set else False
    
            _note_list.append(
                {
                    'entity_context' : _entity_context,
                    'note_context' : _note_context,
                    'creator_context' : _creator_context,
                    'is_user_already_like' : _is_user_already_like
                }
            )
        except Exception, e:
            pass
    
    _duration = datetime.datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds, 
        page='USER_NOTE', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'user_id' : int(user_id),
            'result_notes' : _note_id_list,
        },
    )

    return render_to_response(
        template,
        {
            'content_tab' : 'note',
            'request_user_context' : _request_user_context,
            'query_user_context' : _query_user_context,
            'relation' : _relation,
            'note_list' : _note_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_tags(request, user_id, template=TEMPLATE):
    _start_at = datetime.datetime.now()
    _query_user = User(user_id)
    _query_user_context = _query_user.read()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_context = User(_request_user_id).read() 
        _relation = User.get_relation(_request_user_context['user_id'], _query_user_context['user_id']) 
    else:
        _request_user_id = None 
        _request_user_context = None
        _relation = None 

    _page_num = int(request.GET.get('p', '1'))
    _tag_stat_list = Tag.user_tag_stat(user_id)
    _total_count = len(_tag_stat_list)
    _paginator = Paginator(_page_num, 20, len(_tag_stat_list))

    _tag_list = []
    _log_tags = []
    for _tag_stat in _tag_stat_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _tag_id = _tag_stat['tag_id']
            _tag_hash = _tag_stat['tag_hash']
            _tag = _tag_stat['tag']
            _entity_id_list = Tag.find_user_tag_entity(user_id, _tag)
            _entity_count = len(_entity_id_list)
            _entity_list = [Entity(x).read() for x in _entity_id_list[:4]]
    
            _tag_list.append({
                'tag' : _tag,
                'tag_id' : _tag_id,
                'tag_hash' : _tag_hash,
                'entity_list' : _entity_list,
                'entity_count' : _entity_count
            })
            _log_tags.append(_tag)
        except Exception, e:
            pass
    
    _duration = datetime.datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds, 
        page='USER_TAGS', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'user_id' : int(user_id),
            'result_tags' : _log_tags 
        },
    )

    return render_to_response(
        template,
        {
            'content_tab' : 'tag',
            'request_user_context' : _request_user_context,
            'query_user_context' : _query_user_context,
            'relation' : _relation,
            'tag_list' : _tag_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_followings(request, user_id, template=TEMPLATE):
    # _start_at = datetime.datetime.now()
    _query_user = User(user_id)
    _query_user_context = _query_user.read() 
    if request.user.is_authenticated():
        _request_user_id = request.user.id 
        _request_user_context = User(_request_user_id).read() 
        _relation = User.get_relation(_request_user_context['user_id'], _query_user_context['user_id']) 
    else:
        _request_user_id = None 
        _request_user_context = None
        _relation = None 


    _page_num = request.GET.get('p', 1)
    _following_id_list = _query_user.read_following_user_id_list()
    _total_count = len(_following_id_list)

    _paginator = Paginator(_page_num, 8, len(_following_id_list))
    _following_list = []
    for _u_id in _following_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _f_user = User(_u_id)
            _f_user_context = _f_user.read()
            if _request_user_context != None:
                _f_user_context['relation'] = User.get_relation(_request_user_context['user_id'], _u_id)
            _f_user_context['latest_like_entity_id_list'] = _f_user.read_latest_like_entity_list() 
            _following_list.append(_f_user_context)
        except Exception, e:
            pass
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='USER_FOLLOWINGS',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'user_id' : int(user_id),
    #     },
    # )

    return render_to_response(
        template,
        {
            'content_tab' : 'following',
            'request_user_context' : _request_user_context,
            'query_user_context' : _query_user_context,
            'relation' : _relation,
            'user_list' : _following_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_fans(request, user_id, template=TEMPLATE):
    # _start_at = datetime.datetime.now()
    _query_user = User(user_id)
    _query_user_context = _query_user.read() 
    if request.user.is_authenticated():
        _request_user_id = request.user.id 
        _request_user_context = User(_request_user_id).read() 
        _relation = User.get_relation(_request_user_context['user_id'], _query_user_context['user_id']) 
    else:
        _request_user_id = None 
        _request_user_context = None
        _relation = None 

    _page_num = request.GET.get('p', 1)
    _fans_id_list = _query_user.read_fan_user_id_list()
    _paginator = Paginator(_page_num, 8, len(_fans_id_list))

    _fans_list = []
    for _u_id in _fans_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _f_user = User(_u_id)
            _f_user_context = _f_user.read()
            if _request_user_context != None:
                _f_user_context['relation'] = User.get_relation(_request_user_context['user_id'], _u_id)
            _f_user_context['latest_like_entity_id_list'] = _f_user.read_latest_like_entity_list() 
            _fans_list.append(_f_user_context)
        except Exception, e:
            pass
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='USER_FANS',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'user_id' : int(user_id),
    #     },
    # )

    return render_to_response(
        template,
        {
            'content_tab' : 'fan',
            'request_user_context' : _request_user_context,
            'query_user_context' : _query_user_context,
            'relation' : _relation,
            'user_list' : _fans_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


@login_required
def follow(request, user_id, target_status):
    if request.method == 'POST':
        _followee_id = int(user_id)
        _user = User(request.user.id)

        if _user.is_following(_followee_id):
            _user.unfollow(_followee_id)
            return HttpResponse('0')
        else:
            _user.follow(_followee_id)
            return HttpResponse('1')

def user_tag_entity(request, user_id, tag_hash, template="tag/tag_detail.html"):
    # _start_at = datetime.datetime.now()
    # _request_user_id = request.user.id if request.user.is_authenticated() else None
    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_like_entity_set = Entity.like_set_of_user(_request_user_id)
    else:
        _request_user_id = None
        _request_user_like_entity_set = list()

    _user_context = User(user_id).read()
    _tag_text = Tag.get_tag_text_from_hash(tag_hash)
    
    _page_num = request.GET.get('p', 1)
    
    _entity_id_list = Tag.find_user_tag_entity(user_id, _tag_text)
    _paginator = Paginator(_page_num, 24, len(_entity_id_list))
    
    _entities = list()
    for _entity_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _entity_context = Entity(_entity_id).read()
            _entity_context['is_user_already_like'] = True if _entity_id in _request_user_like_entity_set else False
            _entities.append(_entity_context)
            # _entities.append(Entity(_entity_id).read())
        except Exception, e:
            log.error(e.message)
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='USER_TAG',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'tag' : _tag_text,
    #         'user_id' : int(user_id),
    #         'result_entities' : _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]
    #     },
    # )
    
    return render_to_response(template,
        {
            'tag': _tag_text,
            'entities': _entities,
            'user_context' : _user_context,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )
