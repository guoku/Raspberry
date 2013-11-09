# coding=utf8
from common.message import *
from account import *
from category import *
from entity import *
from note import *
from user import *
import time



def homepage(request):
    _session = request.GET.get('session', None)
    if _session != None:
        _request_user_id = Session_Key.objects.get_user_id(_session)
    else:
        _request_user_id = None
    _rslt = {}
    _rslt['hot'] = []
    _note_id_list = RBMobileNote.find(
        count = 3
    )
    for _note_id in _note_id_list: 
        _note_context = RBMobileNote(_note_id).read(_request_user_id)
        if _note_context.has_key('entity_id'):
            _entity = RBMobileEntity(_note_context['entity_id'])
            _rslt['hot'].append({
                'type' : 'entity',
                'object' : {
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context
                }
            })
    
    _rslt['discover'] = []
    _rslt['discover'].append(RBCategory(103).read())
    _rslt['discover'].append(RBCategory(4).read())
    _rslt['discover'].append(RBCategory(83).read())
    _rslt['discover'].append(RBCategory(12).read())
    _rslt['discover'].append(RBCategory(91).read())
    _rslt['discover'].append(RBCategory(65).read())
    _rslt['discover'].append(RBCategory(116).read())
    _rslt['discover'].append(RBCategory(85).read())
    _rslt['discover'].append(RBCategory(10).read())
    
    return SuccessJsonResponse(_rslt)
     
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
            _following_user_id_list = RBMobileUser(_request_user_id).get_following_user_id_list()
        else:
            _following_user_id_list = None
        
        _note_list = RBMobileEntity.find_entity_note(
            timestamp = _timestamp,
            creator_id_set = _following_user_id_list,
            offset = _offset,
            count = _count
        )
        _note_id_list = map(lambda x: x['note_id'], _note_list)

        
        _rslt = []
        for _note_id in _note_id_list: 
            _note_context = RBMobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = RBMobileEntity(_note_context['entity_id'])
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
        for _message in Message.objects.filter(user_id = _request_user_id, created_time__lt = _timestamp):
            if isinstance(_message, UserFollowMessage):
                _context = {
                    'type' : 'user_follow',
                    'created_time' : time.mktime(_message.created_time.timetuple()),
                    'content': {
                        'follower' : RBMobileUser(_message.follower_id).read(_request_user_id)
                    }
                }
                _rslt.append(_context)
            elif isinstance(_message, NotePokeMessage):
                _context = {
                    'type' : 'note_poke_message',
                    'created_time' : time.mktime(_message.created_time.timetuple()),
                    'content' : {
                        'note' : RBMobileNote(_message.note_id).read(_request_user_id),
                        'poker' : RBMobileUser(_message.poker_id).read(_request_user_id)
                    }
                }
                _rslt.append(_context)
            elif isinstance(_message, NoteCommentMessage):
                _context = {
                    'type' : 'note_comment_message',
                    'created_time' : time.mktime(_message.created_time.timetuple()),
                    'content' : {
                        'note' : RBMobileNote(_message.note_id).read(_request_user_id),
                        #'comment_id' : _message.comment_id,
                        'comment_user' : RBMobileUser(_message.comment_creator_id).read(_request_user_id)
                    }
                }
                _rslt.append(_context)
            elif isinstance(_message, NoteCommentReplyMessage):
                _context = {
                    'type' : 'note_comment_reply_message',
                    'created_time' : time.mktime(_message.created_time.timetuple()),
                    'content' : {
                        'note' : RBMobileNote(_message.note_id).read(_request_user_id),
                        #'comment_id' : _message.comment_id,
                        'replying_user' : RBMobileUser(_message.replying_user_id).read(_request_user_id)
                    }
                }
                _rslt.append(_context)
                
        
        return SuccessJsonResponse(_rslt)
