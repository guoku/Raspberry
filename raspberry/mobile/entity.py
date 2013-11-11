# coding=utf8
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key
import datetime

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
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _entity_id_list = MobileEntity.find(
            timestamp = _timestamp,
            offset = _offset,
            count = _count,
            status = 1
        )
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = MobileEntity(_entity_id)
            _rslt.append(
                _entity.read(_request_user_id)
            )
        return SuccessJsonResponse(_rslt)
    



def category_entity(request, category_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _sort_by = request.GET.get('sort', 'new')
        _reverse = request.GET.get('reverse', '0')
        if _reverse == '0':
            _reverse = False
        else:
            _reverse = True
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _entity_id_list = MobileEntity.find(
            category_id = category_id,
            status = 1,
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
            
        return SuccessJsonResponse(_rslt)


def entity_detail(request, entity_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _rslt = MobileEntity(entity_id).read_full_context(_request_user_id)
        return SuccessJsonResponse(_rslt)
        


def like_entity(request, entity_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 'entity_id' : entity_id }
        if target_status == '1':
            MobileEntity(entity_id).like(_request_user_id)
            _rslt['like_already'] = 1
        else:
            MobileEntity(entity_id).unlike(_request_user_id)
            _rslt['like_already'] = 0
        return SuccessJsonResponse(_rslt)
            

def add_note_for_entity(request, entity_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _note_text = request.POST.get('note', None)
        _score = int(request.POST.get('score', None))
        
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
        _note = _entity.add_note(
            creator_id = _request_user_id,
            note_text = _note_text,
            score = _score,
            image_data = _image_data,
        )
        _context = _note.read(request_user_id = _request_user_id) 
        return SuccessJsonResponse(_context)



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
        
        _rslt = []
        for _entity_id in MobileEntity.like_list_of_user(user_id = user_id, timestamp = _timestamp, offset = _offset, count = _count):
            _rslt.append(MobileEntity(_entity_id).read(_request_user_id))

        return SuccessJsonResponse(_rslt)
    
    
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

