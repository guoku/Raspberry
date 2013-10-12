# coding=utf8
from common.user import RBUser
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 
import time


class RBMobileUser(RBUser):
    
    def __init__(self, user_id):
        RBUser.__init__(self, user_id)

     


def follow_user(request, followee_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 'user_id' : followee_id }
        _request_user = RBMobileUser(_user_id)
        if target_status == '1':
            _request_user.follow(followee_id)
        else:
            _request_user.unfollow(followee_id)
        _rslt['relation'] = _request_user.get_relation(followee_id)
        return SuccessJsonResponse(_rslt)
            

