# coding=utf8
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
        _rslt['status'] = RBMobileUser.get_relation(_request_user_id, _user_id)
        return SuccessJsonResponse(_rslt)


def user_following(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
            _request_user = RBMobileUser(_request_user_id)
            
            _rslt = []
            _following_user_id_list = RBMobileUser(_request_user_id).get_following_user_id_list()
            for _following_user_id in _following_user_id_list: 
                _rslt.append({
                    'entity' : _entity.read(),
                    'note' : _entity.read_note(_note_info['note_id'], _request_user_id)
                })
        
            return SuccessJsonResponse(_rslt)
