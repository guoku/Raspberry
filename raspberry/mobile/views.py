# coding=utf8
from account import *
from candidate import *
from category import *
from entity import *
from note import *
from user import *


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
        else:
            _rslt['hot'].append({
                'type' : 'candidate',
                'object' : {
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
        _type = request.GET.get('type', 'all')
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp)) 
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))

        if _type == 'friend':
            _following_user_id_list = RBMobileUser(_request_user_id).get_following_user_id_list()
        else:
            _following_user_id_list = None

        _note_id_list = RBMobileNote.find(
            timestamp = _timestamp,
            creator_set = _following_user_id_list,
            offset = _offset,
            count = _count
        )
        
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
            elif _note_context.has_key('candidate_id'):
                if _note_context['candidate_weight'] >= 0: 
                    _rslt.append({
                        'type' : 'candidate',
                        'object' : {
                            'note' : _note_context
                        }
                    })
        
        return SuccessJsonResponse(_rslt)
