# coding=utf8
from lib.entity import RBMobileEntity
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
        _last_note = RBMobileEntity.get_user_last_note(user_id)
        if _last_note != None:
            _rslt['last_note'] = RBMobileEntity(_last_note['entity_id']).read_note(_last_note['note_id'], _request_user_id)
        _last_like_entity_id = RBMobileEntity.get_user_last_like(user_id)
        if _last_like_entity_id != None:
            _rslt['last_like'] = RBMobileEntity(_last_like_entity_id).read(_request_user_id)
            
        return SuccessJsonResponse(_rslt)
