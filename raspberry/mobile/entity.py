# coding=utf8
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from lib.sign import check_sign
from mobile.models import Session_Key
from tasks import DeleteEntityNoteTask, LikeEntityTask, UnlikeEntityTask, MobileLogTask
from utils.lib import get_client_ip
import datetime
import time

@check_sign
def entity_list(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _timestamp = request.GET.get('timestamp', None)
        if _timestamp != None:
            _timestamp = datetime.datetime.fromtimestamp(float(_timestamp)) 
        
        _sort_by = request.GET.get('sort', 'updated')
        _reverse = request.GET.get('reverse', '0')
        if _reverse == '0':
            _reverse = False
        else:
            _reverse = True
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        _root_old_cat_id = request.GET.get('rcat', None)
        if _root_old_cat_id != None:
            _root_old_cat_id = int(_root_old_cat_id)
        
        _entity_id_list = MobileEntity.find(
            root_old_category_id = _root_old_cat_id,
            timestamp = _timestamp,
            offset = _offset,
            count = _count,
            sort_by = _sort_by,
            reverse = _reverse,
            status = 'novus' 
        )
        
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = MobileEntity(_entity_id)
            _rslt.append(
                _entity.read(_request_user_id)
            )
        
        MobileLogTask.delay('NOVUS', request.REQUEST, get_client_ip(request), _request_user_id)
        
        return SuccessJsonResponse(_rslt)
    

@check_sign
def search_entity(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        _type = request.GET.get('type', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _query_string = request.GET.get('q')
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _entity_id_list = MobileEntity.search(
            query_string = _query_string,
        )
        _rslt = {
            'stat' : {
                'all_count' : len(_entity_id_list),
                'like_count' : 0,
            },
            'entity_list' : []
        }
       
        if _request_user_id != None:
            _like_set = MobileEntity.like_set_of_user(_request_user_id)
            _like_entity_id_list = _like_set.intersection(_entity_id_list)
            _rslt['stat']['like_count'] = len(_like_entity_id_list)
            if _type == 'like':
                _entity_id_list = list(_like_entity_id_list)

        for _entity_id in _entity_id_list[_offset : _offset + _count]:
            _entity = MobileEntity(_entity_id)
            _rslt['entity_list'].append(
                _entity.read(_request_user_id)
            )
        
        MobileLogTask.delay('SEARCH_ENTITY', request.REQUEST, get_client_ip(request), _request_user_id, { 'query' : _query_string })
        
        return SuccessJsonResponse(_rslt)


@check_sign
def category_entity(request, category_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _sort_by = request.GET.get('sort', None)
        _reverse = request.GET.get('reverse', '0')
        if _reverse == '0':
            _reverse = False
        else:
            _reverse = True
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _entity_id_list = MobileEntity.find(
            category_id = category_id,
            status = 'normal',
            sort_by = _sort_by,
            offset = _offset,
            count = _count,
            reverse = _reverse
        )
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = MobileEntity(_entity_id)
            _rslt.append(
                _entity.read(_request_user_id)
            )
            
        MobileLogTask.delay('CATEGORY_ENTITY', request.REQUEST, get_client_ip(request), _request_user_id, { 'category_id' : int(category_id) })
        return SuccessJsonResponse(_rslt)


@check_sign
def entity_detail(request, entity_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _rslt = MobileEntity(entity_id).read_full_context(_request_user_id)
        
        MobileLogTask.delay('ENTITY', request.REQUEST, get_client_ip(request), _request_user_id, { 'entity_id' : int(entity_id) })
        
        return SuccessJsonResponse(_rslt)
        


@check_sign
def like_entity(request, entity_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 'entity_id' : int(entity_id) }
        if target_status == '1':
            LikeEntityTask.delay(entity_id, _request_user_id)
            _rslt['like_already'] = 1
        else:
            UnlikeEntityTask.delay(entity_id, _request_user_id)
            _rslt['like_already'] = 0
        return SuccessJsonResponse(_rslt)
            

@check_sign
def add_note_for_entity(request, entity_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _note_text = request.POST.get('note', None)
        _score = int(request.POST.get('score', '0'))
        
        _image_file = request.FILES.get('image', None)
        if _image_file == None:
            _image_data = None
        else:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _entity = MobileEntity(entity_id)
        try:
            _note = _entity.add_note(
                creator_id = _request_user_id,
                note_text = _note_text,
                score = _score,
                image_data = _image_data,
            )
        except MobileNote.UserAddNoteForEntityAlready, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'user_add_note_for_entity_already',
                    'message' : str(e)
                },
                status = 400
            )
            
        _context = _note.read(request_user_id = _request_user_id) 
        return SuccessJsonResponse(_context)

@check_sign
def delete_entity_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _entity_id = MobileNote(note_id).get_entity_id()
        DeleteEntityNoteTask.delay(_entity_id, note_id)
        
        return SuccessJsonResponse({ 'delete_already' : 1 })


@check_sign
def user_like(request, user_id):
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
        for _item in MobileEntity.like_list_of_user(user_id = user_id, timestamp = _timestamp, offset = _offset, count = _count):
            _list.append(MobileEntity(_item[0]).read(_request_user_id))
            _last_like_time = _item[1]

        _rslt = {
            'timestamp' : time.mktime(_last_like_time.timetuple()),
            'entity_list' : _list
        }

        MobileLogTask.delay('USER_LIKE', request.REQUEST, get_client_ip(request), _request_user_id, { 'user_id' : int(user_id) })
        return SuccessJsonResponse(_rslt)
    
    
@check_sign
def search(request):
    if request.method == "GET":
        _query = request.GET.get('q', None)
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _rslt = []
        for _entity_id in MobileEntity.search(_query):
            _rslt.append(MobileEntity(_entity_id).read(_request_user_id))
        
        return SuccessJsonResponse(_rslt)


@check_sign
def guess_entity(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _category_id = request.GET.get('cid', None)
        _count = int(request.GET.get('count', '5'))
        if _category_id != None:
            _category_id = int(_category_id)
        _rslt = []
        for _entity_id in MobileEntity.roll(category_id = _category_id, count = _count):
            _rslt.append(MobileEntity(_entity_id).read(_request_user_id))
        
        return SuccessJsonResponse(_rslt)

