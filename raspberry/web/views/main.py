# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.template import RequestContext
from django.template import loader
from django.utils.log import getLogger
# import json
from utils.http import JSONResponse
from datetime import datetime

from utils.paginator import Paginator
from base.message import NeoMessage, UserFollowMessage, NoteSelectionMessage, NoteCommentReplyMessage, NotePokeMessage, NoteCommentMessage, EntityLikeMessage, EntityNoteMessage
# from base.message import *
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.tag import Tag 
from base.user import User
from base.taobao_shop import GuokuPlusActivity
from base.category import Old_Category
import base.popularity as popularity
from base.banner import Banner
from base.category import Category
# from web.tasks import WebLogTask
from utils.lib import get_client_ip
import time

log = getLogger('django')

def index(request):
    return HttpResponseRedirect(reverse('web_selection'))

@require_http_methods(['GET'])
def selection(request, template='main/selection.html'):

    if request.user.is_authenticated():
        _request_user_id = request.user.id
        _request_user_context = User(_request_user_id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        # _request_user_id = None
        _request_user_context = None
        _request_user_like_entity_set = []
     
    _old_category_list = Old_Category.find()[0:11]

    _page_num = request.GET.get('p', 1)
    _time_filter  = request.GET.get('t', datetime.now())
    _category_id = request.GET.get('c', None)
    
    _hdl = NoteSelection.objects.filter(post_time__lt = _time_filter)
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
            log.error(e.message)
	        # print '.............', e.message
            # pass

    # _duration = datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='SELECTION',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'root_category_id' : int(_category_id),
    #         'result_entities' : _entity_id_list,
    #     },
    # )
    # 判断是否第一次加载
    # if _page_num == 1:
    if request.is_ajax():
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
    else:

        return render_to_response(
            template,
            {
                # 'main_nav_deliver' : 'selection',
                'paginator': _paginator,
                'page_num' : _page_num,
                'curr_category_id' : _category_id,
                'user_context' : _request_user_context,
                'category_list' : _old_category_list,
                'selection_list' : _selection_list,
            },
            context_instance = RequestContext(request)
        )
    # else:

@login_required
def web_message(request,  template='main/message.html'):
    # _start_at = datetime.now()

    if request.method == "GET":
        _request_user_id = request.user.id
        _timestamp = request.GET.get('timestamp',None)
        if _timestamp != None:
            _timestamp = datetime.fromtimestamp(float(_timestamp))
        else:
            _timestamp = datetime.now()
        _count = int(request.GET.get('count',30))


        _recommend_tag_list = Tag.get_recommend_user_tag_list()

        # _popular_list = popularity.read_popular_user_context()
        # _popular_list_detail = []
        # if _popular_list != None:
        #     for _popular_user in _popular_list["data"]:
        #         try:
        #             _popu_context = {
        #                 "user_id" : _popular_user["user_id"],
        #                 "user_context" : User(_popular_user["user_id"]).read(),
        #                 "relation" : User.get_relation(_request_user_id,_popular_user["user_id"])
        #             }
        #             _popular_list_detail.append(_popu_context)
        #         except Exception, e:
        #             log.error(e.message)

        _rslt = []
        for _message in NeoMessage.objects.filter(user_id=_request_user_id,created_time__lt=_timestamp).order_by('-created_time')[0:_count]:
            try:
                if isinstance(_message, UserFollowMessage):
                    _context = {
                        'type' : 'user_follow',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content': {
                            'follower' : User(_message.follower_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NotePokeMessage):
                    _context = {
                        'type' : 'note_poke_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'note' : Note(_message.note_id).read(_request_user_id),
                            'poker' : User(_message.poker_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteCommentMessage):
                    _context = {
                        'type' : 'note_comment_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'note' : Note(_message.note_id).read(_request_user_id),
                            'comment' : Note(_message.note_id).read_comment(_message.comment_id),
                            'comment_user' : User(_message.comment_creator_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteCommentReplyMessage):
                    _context = {
                        'type' : 'note_comment_reply_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'note' : Note(_message.note_id).read(_request_user_id),
                            'comment' : Note(_message.note_id).read_comment(_message.comment_id),
                            'replying_comment' : Note(_message.note_id).read_comment(_message.replying_comment_id),
                            'replying_user' : User(_message.replying_user_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, EntityLikeMessage):
                    _context = {
                        'type' : 'entity_like_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'liker' : User(_message.liker_id).read(_request_user_id),
                            'entity' : Entity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, EntityNoteMessage):
                    _context = {
                        'type' : 'entity_note_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'note' : Note(_message.note_id).read(_request_user_id),
                            'entity' : Entity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteSelectionMessage):
                    _context = {
                        'type' : 'note_selection_message',
                        'created_time' : datetime.fromtimestamp(time.mktime(_message.created_time.timetuple())),
                        'content' : {
                            'note' : Note(_message.note_id).read(_request_user_id),
                            'entity' : Entity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
            except Exception, e:
                log.error(e.message)

        if request.is_ajax():
            # template = 'main/partial/ajax_message.html'
            _ret = {
                'status' : 0,
                'msg' : '没有更多数据'
            }
            if len(_rslt) > 0:
                _t = loader.get_template('main/partial/ajax_message.html')
                _c = RequestContext(request, {
                    'message_list': _rslt,
                })
                _data = _t.render(_c)
                _ret = {
                    'status' : '1',
                    'data' : _data
                }
            return JSONResponse(_ret)
        # log.info(_rslt)
        return render_to_response(
            template,
            {
                'message_list' : _rslt,
                'recommend_tag_list' : _recommend_tag_list,
                # 'popular_list' : _popular_list_detail
            },
            context_instance = RequestContext(request)
        )
       

def wap_selection(request, template='wap/selection.html'):

    return HttpResponseRedirect(reverse('web_selection'))


def tencent_selection(request, template='tencent/selection.html'):
    return HttpResponseRedirect(reverse('web_selection'))




@require_http_methods(['GET'])
def popular(request, template='main/popular.html'):
    # _start_at = datetime.now()
    if request.user.is_authenticated():
        # _request_user_id = request.user.id
        _request_user_context = User(request.user.id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        # _request_user_id = None
        _request_user_context = None
        _request_user_like_entity_set = [] 
    
    _group = request.GET.get('group', 'daily')
    _popular_list = []
    _entity_id_list = []
    _popular_updated_time = datetime.now() 
   
    _popular_entities = popularity.read_popular_entity_from_cache(scale=_group)
    # log.info(_popular_entities)
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
                _entity_id_list.append(_entity_id)
            except Exception, e:
                pass
    
    if _group== 'weekly':
        _log_appendix = { 'scale' : 'WEEK' }
    else:
        _log_appendix = { 'scale' : 'DAY' }
    _log_appendix['result_entities'] = _entity_id_list
    # _duration = datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='POPULAR',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix=_log_appendix
    # )

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


@require_GET
def popular_category(request, template="main/popular_category.html"):
    _banners = Banner.find(status = 'active')

    _kinds = Category.all_group_with_full_category()
    log.info(_kinds)
    return render_to_response(
        template,
        {
            'banners': _banners,
            'kinds': _kinds,
        },
        context_instance=RequestContext(request)
    )

@require_POST
@login_required
def get_guokuplus_token(request):
    activity_id = request.POST.get("activity_id", None)
    if activity_id:
        guokuplus = GuokuPlusActivity(int(activity_id))
        token_context = guokuplus.get_token(request.user.id)
        return HttpResponse(token_context['token'])
    return HttpResponse("error")
