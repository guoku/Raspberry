# coding=utf8
from base.banner import Banner
from base.message import *
from base.models import Selection, NoteSelection 
import base.popularity as popularity 
from django.core.urlresolvers import reverse
from django.conf import settings
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from account import *
from category import *
from entity import *
from note import *
from report import *
from user import *
import time


def homepage(request):
    _session = request.GET.get('session', None)
    if _session != None:
        _request_user_id = Session_Key.objects.get_user_id(_session)
    else:
        _request_user_id = None
    _rslt = {}
    _rslt['discover'] = Category.find(offset = 0, count = 8, order_by = '-status') 
    
    _rslt['banner'] = []
    for _banner_context in Banner.find():
        _rslt['banner'].append({
            'url' : _banner_context['url'], 
            'img' : _banner_context['image'] 
        })
    
    if settings.JUMP_TO_TAOBAO: 
        _rslt['jump_to_taobao'] = 1
    else:
        _rslt['jump_to_taobao'] = 0
        
    
    return SuccessJsonResponse(_rslt)

from base.models import Seed_User
def feed(request):
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
            #MobileUser(_request_user_id).mark_footprint(friend_feed = True)
        else:
            _following_user_id_list = map(lambda x: x.user_id, Seed_User.objects.all())
            #MobileUser(_request_user_id).mark_footprint(social_feed = True)
        
        _note_id_list = MobileNote.find(
            timestamp = _timestamp,
            creator_set = _following_user_id_list,
            offset = _offset,
            count = _count
        )

        
        _rslt = []
        for _note_id in _note_id_list: 
            _note_context = MobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = MobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'type' : 'entity',
                    'object' : {
                        'entity' : _entity.read(_request_user_id),
                        'note' : _note_context
                    }
                })
        
        return SuccessJsonResponse(_rslt)

def message(request):
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
        for _message in NeoMessage.objects.filter(user_id = _request_user_id, created_time__lt = _timestamp).order_by('-created_time'):
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
               
        return SuccessJsonResponse(_rslt)

def selection(request):
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
        
        #MobileUser(_request_user_id).mark_footprint(selection = True)
        
        return SuccessJsonResponse(_rslt)

def popular(request):
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
            for _row in _popular_entities['data'][0:60]:
                _entity_id = _row[0]
                _hotness = _row[1] 
                _entity_context = MobileEntity(_entity_id).read(_request_user_id)
                _rslt['content'].append({
                    'entity' : _entity_context,
                    'hotness' : _hotness
                })
            return SuccessJsonResponse(_rslt)
        else:
            return ErrorJsonResponse(
                data = {
                    'type' : 'no_popular_data',
                    'message' : 'no popular data' 
                },
                status = 400
            )

def unread_message_count(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        _request_user_id = Session_Key.objects.get_user_id(_session)
        return SuccessJsonResponse({
            'count' : MobileUser(_request_user_id).get_unread_message_count()
        })
        
