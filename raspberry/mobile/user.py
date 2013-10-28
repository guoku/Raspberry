# coding=utf8
from lib.entity import RBMobileEntity
from lib.note import RBMobileNote
from lib.user import RBMobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 
    

def follow_user(request, user_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        
        _user_id = int(user_id)
        _rslt = { 'user_id' : _user_id }
        if target_status == '1':
            RBMobileUser(_request_user_id).follow(_user_id)
        else:
            RBMobileUser(_request_user_id).unfollow(_user_id)
        _rslt['relation'] = RBMobileUser.get_relation(_request_user_id, _user_id)
        return SuccessJsonResponse(_rslt)


def user_following(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
            _request_user = RBMobileUser(_request_user_id)
            
            _rslt = []
            _following_user_id_list = RBMobileUser(user_id).get_following_user_id_list()
            
            for _following_user_id in _following_user_id_list: 
                _rslt.append(RBMobileUser(_following_user_id).read(_request_user_id))
        
            return SuccessJsonResponse(_rslt)

def user_fan(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
            _request_user = RBMobileUser(_request_user_id)
            
            _rslt = []
            _fan_user_id_list = RBMobileUser(user_id).get_fan_user_id_list()
            
            for _fan_user_id in _fan_user_id_list: 
                _rslt.append(RBMobileUser(_fan_user_id).read(_request_user_id))
        
            return SuccessJsonResponse(_rslt)

def user_detail(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
            
        _rslt = {}
        _rslt['user'] = RBMobileUser(user_id).read_full_context(_request_user_id)
        _last_note_id = RBMobileNote.get_user_last_note(user_id)
        if _last_note_id != None:
            _rslt['last_note'] = RBMobileNote(_last_note_id).read(_request_user_id)
        _last_like_entity_id = RBMobileEntity.get_user_last_like(user_id)
        if _last_like_entity_id != None:
            _rslt['last_like'] = RBMobileEntity(_last_like_entity_id).read(_request_user_id)
            
        return SuccessJsonResponse(_rslt)

def upload_user_avatar(request):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
    
        _image_file = request.FILES.get('image', None)
        if hasattr(_image_file, 'chunks'):
            _image_data = ''.join(chunk for chunk in _image_file.chunks())
        else:
            _image_data = _image_file.read()
        
        _user = RBMobileUser(_request_user_id)
        _user.upload_avatar(_image_data)
        return SuccessJsonResponse(_user.read())

def user_entity_note(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = []
        for _entity_note_obj in RBMobileEntity.find_entity_note(creator_id = user_id):
            _note_context = RBMobileNote(_entity_note_obj['note_id']).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = RBMobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context, 
                })

        return SuccessJsonResponse(_rslt)
