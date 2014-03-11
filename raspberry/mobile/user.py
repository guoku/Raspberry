# coding=utf8
from base.tag import *
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from lib.sign import check_sign
from mobile.models import Session_Key
from tasks import FollowUserTask, UnfollowUserTask, MobileLogTask
from utils.lib import get_client_ip
import datetime
import time    

@check_sign
def category_user_like(request, category_id, user_id):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        _sort_by = request.GET.get('sort', 'new')
        _reverse = request.GET.get('reverse', '0')
        if _reverse == '0':
            _reverse = False
        else:
            _reverse = True
        
        _entity_id_list = MobileUser(user_id).find_like_entity(
            neo_category_id = category_id,
            offset = _offset,
            count = _count,
            sort_by = _sort_by,
            reverse = _reverse
        )
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = MobileEntity(_entity_id)
            _rslt.append(
                _entity.read(_request_user_id)
            )
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'CATEGORY_USER_LIKE', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'neo_category_id' : int(category_id),
                'user_id' : int(user_id),
                'result_entities' : _entity_id_list
            },
        )
        return SuccessJsonResponse(_rslt)



@check_sign
def follow_user(request, user_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        
        _user_id = int(user_id)
        _rslt = { 'user_id' : _user_id }
        _rslt['relation'] = MobileUser.get_relation(_request_user_id, _user_id)
        if target_status == '1':
            FollowUserTask.delay(_request_user_id, _user_id)
            if _rslt['relation'] == 0:
                _rslt['relation'] = 1
            elif _rslt['relation'] == 2:
                _rslt['relation'] = 3
        else:
            UnfollowUserTask.delay(_request_user_id, _user_id)
            if _rslt['relation'] == 3:
                _rslt['relation'] = 2
            elif _rslt['relation'] == 1:
                _rslt['relation'] = 0
        return SuccessJsonResponse(_rslt)


@check_sign
def user_following(request, user_id):
    _start_at = datetime.datetime.now()
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
    
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_FOLLOWING', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'result_users' : _following_user_id_list[_offset : _offset + _count]
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def user_fan(request, user_id):
    _start_at = datetime.datetime.now()
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
    
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_FAN', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'result_users' : _fan_user_id_list[_offset : _offset + _count]
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def user_info(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _rslt = MobileUser(_request_user_id).read()
        return SuccessJsonResponse(_rslt)


@check_sign
def user_detail(request, user_id):
    _start_at = datetime.datetime.now()
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
            
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
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

@check_sign
def user_entity_note(request, user_id):
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
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _rslt = []
        _note_id_list = MobileNote.find(creator_set = [user_id], timestamp = _timestamp, offset = _offset, count = _count)
        for _note_id in _note_id_list: 
            try:
                _note_context = MobileNote(_note_id).read(_request_user_id)
                if _note_context.has_key('entity_id'):
                    _entity = MobileEntity(_note_context['entity_id'])
                    _rslt.append({
                        'entity' : _entity.read(_request_user_id),
                        'note' : _note_context, 
                    })
            except:
                pass

        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_NOTE', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'result_notes' : _note_id_list
            },
        )
        return SuccessJsonResponse(_rslt)

#@check_sign
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

@check_sign
def random_user_tag(request):
    if request.method == "GET":
        _count = int(request.GET.get('count', '10'))
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = []
        _recommend_user_tag_list = Tag.get_recommend_user_tag_list()
        if len(_recommend_user_tag_list) > _count:
            _recommend_user_tag_list = random.sample(_recommend_user_tag_list, _count)
        for _tag_data in _recommend_user_tag_list:
            _data = {
                'tag_name' : _tag_data[1],
                'entity_count' : _tag_data[2],
                'user' : MobileUser(_tag_data[0]).read(_request_user_id),
                'entity_list' : []
            }
            for _entity_id in Tag.find_user_tag_entity(_tag_data[0], _tag_data[1])[0:3]:
                _data['entity_list'].append(MobileEntity(_entity_id).read(_request_user_id))
            _rslt.append(_data)
        return SuccessJsonResponse(_rslt)
        


@check_sign
def user_tag_list(request, user_id):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _user_context = MobileUser(user_id).read()
        _tag_list = Tag.user_tag_stat(user_id)
        _rslt = {
            'user' : _user_context,
            'tags' : _tag_list
        }
    
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_TAG', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'result_tags' : map(lambda x: x['tag'], _tag_list)
            },
        )
        return SuccessJsonResponse(_rslt)


@check_sign
def user_tag_entity(request, user_id, tag):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _user_context = MobileUser(user_id).read(_request_user_id)
        _entity_id_list = Tag.find_user_tag_entity(user_id, tag)
        _rslt = {
            'user' : _user_context,
            'entity_list' : []
        }
        for _entity_id in _entity_id_list: 
            _rslt['entity_list'].append(MobileEntity(_entity_id).read(_request_user_id))
    
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_TAG_ENTITY', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'tag' : tag 
            },
        )
        return SuccessJsonResponse(_rslt)


#@check_sign
def user_like(request, user_id):
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
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _list = []
        _last_like_time = None
        _entity_id_list = []
        for _item in MobileUser(user_id).find_like_entity(timestamp = _timestamp, offset = _offset, count = _count, with_timestamp = True):
            _list.append(MobileEntity(_item[0]).read(_request_user_id))
            _entity_id_list.append(_item[0])
            _last_like_time = _item[1]
        
        if _last_like_time == None:
            _timestamp = 0.0 
        else:
            _timestamp = time.mktime(_last_like_time.timetuple())
        _rslt = {
            'timestamp' : _timestamp, 
            'entity_list' : _list
        }

        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'USER_LIKE', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'user_id' : int(user_id),
                'result_entities' : _entity_id_list
            },
        )
        return SuccessJsonResponse(_rslt)
    
@check_sign
def search_user(request):
    _start_at = datetime.datetime.now()
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
            query_string = _query_string,
            offset = _offset,
            count = _count
        )
        _rslt = [] 
        for _user_id in _user_id_list: 
            _rslt.append(MobileUser(_user_id).read(_request_user_id))
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'SEARCH_USER', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'query' : _query_string, 
                'result_users' : _user_id_list
            },
        )
        return SuccessJsonResponse(_rslt)
        
