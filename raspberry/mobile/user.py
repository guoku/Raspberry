# coding=utf8
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 
import datetime
    

def follow_user(request, user_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        
        _user_id = int(user_id)
        _rslt = { 'user_id' : _user_id }
        if target_status == '1':
            MobileUser(_request_user_id).follow(_user_id)
        else:
            MobileUser(_request_user_id).unfollow(_user_id)
        _rslt['relation'] = MobileUser.get_relation(_request_user_id, _user_id)
        return SuccessJsonResponse(_rslt)


def user_following(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
            
        _rslt = []
        _following_user_id_list = MobileUser(user_id).read_following_user_id_list()
        for _following_user_id in _following_user_id_list[_offset : _offset + _count]: 
            _rslt.append(MobileUser(_following_user_id).read(_request_user_id))
    
        return SuccessJsonResponse(_rslt)

def user_fan(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
            
        _rslt = []
        _fan_user_id_list = MobileUser(user_id).read_fan_user_id_list()
        for _fan_user_id in _fan_user_id_list[_offset : _offset + _count]: 
            _rslt.append(MobileUser(_fan_user_id).read(_request_user_id))
    
        return SuccessJsonResponse(_rslt)

def user_detail(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
            
        _rslt = {}
        _rslt['user'] = MobileUser(user_id).read(_request_user_id)
        _last_note_id = MobileNote.get_user_last_note(user_id)
        if _last_note_id != None:
            _rslt['last_note'] = MobileNote(_last_note_id).read(_request_user_id)
        _last_like_entity_id = MobileEntity.get_user_last_like(user_id)
        if _last_like_entity_id != None:
            _rslt['last_like'] = MobileEntity(_last_like_entity_id).read(_request_user_id)
            
        return SuccessJsonResponse(_rslt)

def update_user(request):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
    
        _user = MobileUser(_request_user_id)
        
        _image_file = request.FILES.get('image', None)
        if _image_file != None:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
            _user.upload_avatar(_image_data)

        _nickname = request.POST.get('nickname', None)
        _email = request.POST.get('email', None)
        _username = request.POST.get('username', None)
        _password = request.POST.get('password', None)
        if _email != None or _username != None or _password != None:
            _user.reset_account(
                username = _username,
                password = _password,
                email = _email
            )
        
        if _nickname != None:
            _user.set_profile(nickname = _nickname)
        
        return SuccessJsonResponse(_user.read())

def user_entity_note(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp))
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _rslt = []
        for _note_id in MobileNote.find(creator_set = [user_id], timestamp = _timestamp, offset = _offset, count = _count):
            _note_context = MobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = MobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context, 
                })

        return SuccessJsonResponse(_rslt)

def check_sina_user(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _sina_id_list = request.GET.getlist('sid[]')
        _sina_user_list = MobileUser.check_sina_id(_sina_id_list)
        _rslt = [] 
        for _sina_user in _sina_user_list[0:100]:
            _user_id = _sina_user['user_id']
            _rslt.append(MobileUser(_user_id).read(_request_user_id))
        
        return SuccessJsonResponse(_rslt)

def search_user(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _query_string = request.GET.get('q')
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        _user_id_list = MobileUser.search(
            query_string = _query_string
        )
        _rslt = [] 
        for _user_id in _user_id_list: 
            _rslt.append(MobileUser(_user_id).read(_request_user_id))
        
        return SuccessJsonResponse(_rslt)
        
