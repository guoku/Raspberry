# coding=utf8
from base.banner import Banner
from base.message import *
from base.models import Selection, NoteSelection 
import base.popularity as popularity 
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.lib.sign import check_sign
from base.tag import *
from account import *
from category import *
from entity import *
from note import *
from report import *
from user import *
from base.item import Item,JDItem
from share.tasks import MarkFootprint
from tasks import MobileLogTask
from utils.lib import get_client_ip
from utils.taobao import * 
from utils.jd import decorate_jd_url, get_jd_url
from utils.taobaoapi.utils import taobaoke_mobile_item_convert 
import random 
import time

@check_sign
def homepage(request):
    _start_at = datetime.datetime.now()
    _session = request.GET.get('session', None)
    if _session != None:
        _request_user_id = Session_Key.objects.get_user_id(_session)
    else:
        _request_user_id = None

    _log_appendix = {}

    _rslt = {}
    _rslt['discover'] = popularity.read_popular_category()['data'][0:12]
    _log_appendix['discover'] = map(lambda x: x['category_id'], _rslt['discover'])
    
    _rslt['banner'] = []
    _log_appendix['banner'] = []
    for _banner_context in Banner.find(status = 'active'):
        try:
            _rslt['banner'].append({
                'url' : _banner_context['url'], 
                'img' : _banner_context['image'] 
            })
            _log_appendix['banner'].append(_banner_context['banner_id'])
        except Exception, e:
            pass
    

    _rslt['hottag'] = []
    _log_appendix['hottag'] = []
    _recommend_user_tag_list = Tag.get_recommend_user_tag_list()
    if len(_recommend_user_tag_list) > 3:
        _recommend_user_tag_list = random.sample(_recommend_user_tag_list, 3)
    for _tag_data in _recommend_user_tag_list:
        _rslt['hottag'].append({
            'tag_name' : _tag_data[1],
            'entity_count' : _tag_data[2],
            'user' : MobileUser(_tag_data[0]).read(_request_user_id)
        })
        _log_appendix['hottag'].append([_tag_data[0], _tag_data[1]])
    
    _rslt['config'] = {}
    _rslt['config']['taobao_ban_count'] = 2
    _rslt['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']


#    if settings.JUMP_TO_TAOBAO: 
#        _rslt['config']['jump_to_taobao'] = 1
#    else:
#        _rslt['config']['jump_to_taobao'] = 0
    
        
    _duration = datetime.datetime.now() - _start_at
    MobileLogTask.delay(
        duration = _duration.seconds * 1000000 + _duration.microseconds, 
        view = 'HOMEPAGE', 
        request = request.REQUEST, 
        ip = get_client_ip(request), 
        log_time = datetime.datetime.now(),
        request_user_id = _request_user_id,
        appendix = _log_appendix 
    )
    return SuccessJsonResponse(_rslt)

@check_sign
def feed(request):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        _type = request.GET.get('type', 'entity')
        _scale = request.GET.get('scale', 'all')
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp)) 
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        

        if _scale == 'friend':
            _following_user_id_list = MobileUser(_request_user_id).read_following_user_id_list()
            _log_appendix = { 'scale' : 'FRIEND' }
            #MobileUser(_request_user_id).mark_footprint(friend_feed = True)
        else:
            _following_user_id_list = MobileUser.read_seed_users()
            _log_appendix = { 'scale' : 'SOCIAL' }
            #MobileUser(_request_user_id).mark_footprint(social_feed = True)
        
        _note_id_list = MobileNote.find(
            timestamp=_timestamp,
            creator_set=_following_user_id_list,
            offset=_offset,
            count=_count
        )
        _log_appendix['result_notes'] = _note_id_list

        
        _rslt = []
        for _note_id in _note_id_list:
            try:
                _note_context = MobileNote(_note_id).read(_request_user_id)
                if _note_context.has_key('entity_id'):
                    _entity = MobileEntity(_note_context['entity_id'])
                    _rslt.append({
                        'type' : 'entity',
                        'content' : {
                            'entity' : _entity.read(_request_user_id),
                            'note' : _note_context
                        }
                    })
            except Exception, e:
                pass
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'FEED', 
            request = request.REQUEST, 
            ip = get_client_ip(request),
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = _log_appendix 
        )
        
        return SuccessJsonResponse(_rslt)

@check_sign
def message(request):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp))
        else:
            _timestamp = datetime.datetime.now()
        _count = int(request.GET.get('count', '30'))


        _rslt = []
        for _message in NeoMessage.objects.filter(user_id=_request_user_id, created_time__lt=_timestamp).order_by('-created_time')[0:_count]:
            try:
                if isinstance(_message, UserFollowMessage):
                    _context = {
                        'type' : 'user_follow',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content': {
                            'follower' : MobileUser(_message.follower_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NotePokeMessage):
                    _context = {
                        'type' : 'note_poke_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'note' : MobileNote(_message.note_id).read(_request_user_id),
                            'poker' : MobileUser(_message.poker_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteCommentMessage):
                    _context = {
                        'type' : 'note_comment_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'note' : MobileNote(_message.note_id).read(_request_user_id),
                            'comment' : MobileNote(_message.note_id).read_comment(_message.comment_id),
                            'comment_user' : MobileUser(_message.comment_creator_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteCommentReplyMessage):
                    _context = {
                        'type' : 'note_comment_reply_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'note' : MobileNote(_message.note_id).read(_request_user_id),
                            'comment' : MobileNote(_message.note_id).read_comment(_message.comment_id),
                            'replying_comment' : MobileNote(_message.note_id).read_comment(_message.replying_comment_id),
                            'replying_user' : MobileUser(_message.replying_user_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, EntityLikeMessage):
                    _context = {
                        'type' : 'entity_like_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'liker' : MobileUser(_message.liker_id).read(_request_user_id),
                            'entity' : MobileEntity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, EntityNoteMessage):
                    _context = {
                        'type' : 'entity_note_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'note' : MobileNote(_message.note_id).read(_request_user_id),
                            'entity' : MobileEntity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
                elif isinstance(_message, NoteSelectionMessage):
                    _context = {
                        'type' : 'note_selection_message',
                        'created_time' : time.mktime(_message.created_time.timetuple()),
                        'content' : {
                            'note' : MobileNote(_message.note_id).read(_request_user_id),
                            'entity' : MobileEntity(_message.entity_id).read(_request_user_id)
                        }
                    }
                    _rslt.append(_context)
            except:
                # TODO : logger
                pass
            
        if _request_user_id != None:
            MarkFootprint.delay(user_id = _request_user_id, message = True)
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'MESSAGE', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def selection(request):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp))
        else:
            _timestamp = datetime.datetime.now()
        _count = int(request.GET.get('count', '30'))
        _root_cat_id = int(request.GET.get('rcat', '0'))

        _hdl = NoteSelection.objects.filter(post_time__lt = _timestamp)
        if _root_cat_id > 0 and _root_cat_id < 12:
            _hdl = _hdl.filter(root_category_id = _root_cat_id)
        

        _rslt = []
        _entity_id_list = []
        for _selection in _hdl.order_by('-post_time')[0:30]:
            if isinstance(_selection, NoteSelection):
                _context = {
                    'type' : 'note_selection',
                    'post_time' : time.mktime(_selection.post_time.timetuple()),
                    'content': {
                        'entity' : MobileEntity(_selection.entity_id).read(_request_user_id),
                        'note' : MobileNote(_selection.note_id).read(_request_user_id),
                    }
                }
                _rslt.append(_context)
                _entity_id_list.append(_selection.entity_id)
        
        if _request_user_id != None:
            MarkFootprint.delay(user_id = _request_user_id, selection = True)
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'SELECTION', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'root_category_id' : int(_root_cat_id),
                'result_entities' : _entity_id_list,
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def popular(request):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _scale = request.GET.get('scale', 'daily')

        _popular_entities = popularity.read_popular_entity_from_cache(scale = _scale, json = True)
        if _popular_entities != None:
            _rslt = {
                'scale' : _scale,
                'updated_time' : _popular_entities['updated_time'],
                'content' : []
            }
            _entity_id_list = []
            for _row in _popular_entities['data'][0:60]:
                _entity_id = _row[0]
                _hotness = _row[1] 
                _entity_context = MobileEntity(_entity_id).read(_request_user_id)
                _rslt['content'].append({
                    'entity' : _entity_context,
                    'hotness' : _hotness
                })
                _entity_id_list.append(_entity_id)
            
            if _scale == 'weekly':
                _log_appendix = { 'scale' : 'WEEK' }
            else:
                _log_appendix = { 'scale' : 'DAY' }
            _log_appendix['result_entities'] = _entity_id_list
                
            _duration = datetime.datetime.now() - _start_at
            MobileLogTask.delay(
                duration = _duration.seconds * 1000000 + _duration.microseconds, 
                view = 'POPULAR', 
                request = request.REQUEST, 
                ip = get_client_ip(request), 
                log_time = datetime.datetime.now(),
                request_user_id = _request_user_id,
                appendix =  _log_appendix 
            )
            return SuccessJsonResponse(_rslt)
        else:
            return ErrorJsonResponse(
                data = {
                    'type' : 'no_popular_data',
                    'message' : 'no popular data' 
                },
                status = 400
            )

@check_sign
def unread_count(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        _request_user_id = Session_Key.objects.get_user_id(_session)
        return SuccessJsonResponse({
            'unread_message_count' : MobileUser(_request_user_id).get_unread_message_count(),
            'unread_selection_count' : MobileUser(_request_user_id).get_unread_selection_count()
        })
        
def visit_item(request, item_id):
    _start_at = datetime.datetime.now()
    
    if item_id == '533bd0caa2128a11428c912b':
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            entry="jd_bilang",
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'CLICK', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = {}
        )
        return HttpResponseRedirect("http://item.jd.com/1076756.html")
        
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _ttid = request.GET.get("ttid", None)
        _sid = request.GET.get("sid", None)
        _entry = request.GET.get("entry", "mobile")
        _outer_code = request.GET.get("outer_code", None)
        _sche = request.GET.get("sche", None)
        _item_context = Item(item_id).read()
        if _item_context == None:
            return visit_jd_item(request, item_id)
        _taobaoke_info = taobaoke_mobile_item_convert(_item_context['taobao_id'])
        _entity_id = _item_context['entity_id'] if _item_context.has_key('entity_id') else -1 
        _duration = datetime.datetime.now() - _start_at
        
       	if _taobaoke_info and _taobaoke_info.has_key('click_url'):
            MobileLogTask.delay(
                entry=_entry,
                duration = _duration.seconds * 1000000 + _duration.microseconds, 
                view = 'CLICK', 
                request = request.REQUEST, 
                ip = get_client_ip(request), 
                log_time = datetime.datetime.now(),
                request_user_id = _request_user_id,
                appendix = {
                    'site' : 'taobao',
                    'taobao_id' : _item_context['taobao_id'],
                    'item_id' : item_id, 
                    'entity_id' : _entity_id,
                    'tbk' : True,
                }
            )
            return HttpResponseRedirect(decorate_taobao_url(_taobaoke_info['click_url'], _ttid, _sid, _outer_code, _sche))
        
        MobileLogTask.delay(
            entry=_entry,
            duration=_duration.seconds * 1000000 + _duration.microseconds, 
            view='CLICK', 
            request=request.REQUEST, 
            ip=get_client_ip(request), 
            log_time=datetime.datetime.now(),
            request_user_id=_request_user_id,
            appendix={
                'site': 'taobao',
                'taobao_id': _item_context['taobao_id'],
                'entity_id': _entity_id,
                'tbk': False,
            }
        )
        return HttpResponseRedirect(decorate_taobao_url(get_taobao_url(_item_context['taobao_id'], True), _ttid, _sid, _outer_code, _sche))
            


def visit_jd_item(request, item_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _ttid = request.GET.get("ttid", None)
        _sid = request.GET.get("sid", None)
        _entry = request.GET.get("entry", "mobile")
        _outer_code = request.GET.get("outer_code", None)
        _sche = request.GET.get("sche", None)

        _item_context = JDItem(item_id).read()
        buy_link = get_jd_url(_item_context['jd_id'], is_mobile=True)
        return HttpResponseRedirect(decorate_jd_url(buy_link))

######### Old visit item api ######
######### Should be obsolete after all client ends shift to 3.0 ######

def old_visit_item(request):
    _start_at = datetime.datetime.now()
    
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _ttid = request.GET.get("ttid", None)
        _sid = request.GET.get("sid", None)
        _entry = request.GET.get("entry", "mobile")
        _outer_code = request.GET.get("outer_code", None)
        _sche = request.GET.get("sche", None)
        
        _taobao_id = request.GET.get("item_id", None)
        _item = Item.get_item_by_taobao_id(_taobao_id)
        _item_context = _item.read()
    
        if _taobao_id == '38232357603':
            _duration = datetime.datetime.now() - _start_at
            MobileLogTask.delay(
                entry="jd_bilang",
                duration = _duration.seconds * 1000000 + _duration.microseconds, 
                view = 'CLICK', 
                request = request.REQUEST, 
                ip = get_client_ip(request), 
                log_time = datetime.datetime.now(),
                request_user_id = _request_user_id,
                appendix = {}
            )
            return HttpResponseRedirect("http://item.jd.com/1076756.html")
        
        _taobaoke_info = taobaoke_mobile_item_convert(_item_context['taobao_id'])
        _entity_id = _item_context['entity_id'] if _item_context.has_key('entity_id') else -1 
        _duration = datetime.datetime.now() - _start_at
        
       	if _taobaoke_info and _taobaoke_info.has_key('click_url'):
            MobileLogTask.delay(
                entry=_entry,
                duration = _duration.seconds * 1000000 + _duration.microseconds, 
                view = 'CLICK', 
                request = request.REQUEST, 
                ip = get_client_ip(request), 
                log_time = datetime.datetime.now(),
                request_user_id = _request_user_id,
                appendix = {
                    'site' : 'taobao',
                    'taobao_id' : _item_context['taobao_id'],
                    'item_id' : _item_context['item_id'], 
                    'entity_id' : _entity_id,
                    'tbk' : True,
                }
            )
            return HttpResponseRedirect(decorate_taobao_url(_taobaoke_info['click_url'], _ttid, _sid, _outer_code, _sche))
        
        MobileLogTask.delay(
            entry=_entry,
            duration=_duration.seconds * 1000000 + _duration.microseconds, 
            view='CLICK', 
            request=request.REQUEST, 
            ip=get_client_ip(request), 
            log_time=datetime.datetime.now(),
            request_user_id=_request_user_id,
            appendix={
                'site': 'taobao',
                'taobao_id': _item_context['taobao_id'],
                'item_id' : _item_context['item_id'], 
                'entity_id': _entity_id,
                'tbk': False,
            }
        )
        return HttpResponseRedirect(decorate_taobao_url(get_taobao_url(_item_context['taobao_id'], True), _ttid, _sid, _outer_code, _sche))
            

