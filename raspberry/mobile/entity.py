# coding=utf8
from lib.entity import RBMobileEntity
from lib.note import RBMobileNote
from lib.user import RBMobileUser
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
        
        _entity_id_list = RBMobileEntity.find(
            timestamp = _timestamp,
            offset = _offset,
            count = _count
        )
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = RBMobileEntity(_entity_id)
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

        
        _entity_id_list = RBMobileEntity.find(
            category_id = category_id,
            sort_by = _sort_by,
            reverse = _reverse
        )
        _rslt = []
        for _entity_id in _entity_id_list:
            _entity = RBMobileEntity(_entity_id)
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

        _rslt = RBMobileEntity(entity_id).read_full_context(_request_user_id)
        return SuccessJsonResponse(_rslt)
        


def like_entity(request, entity_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 'entity_id' : entity_id }
        if target_status == '1':
            RBMobileEntity(entity_id).like(_request_user_id)
            _rslt['like_already'] = 1
        else:
            RBMobileEntity(entity_id).unlike(_request_user_id)
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
        _entity = RBMobileEntity(entity_id)
        _note = _entity.add_note(
            creator_id = _request_user_id,
            score = _score,
            note_text = _note_text,
            image_data = _image_data,
        )
        _context = _note.read() 
        return SuccessJsonResponse(_context)



def user_like(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = []
        for _entity_id in RBMobileEntity.like_list_of_user(user_id):
            _rslt.append(RBMobileEntity(_entity_id).read(_request_user_id))

        return SuccessJsonResponse(_rslt)
    
def user_note(request, user_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = []
        for _note_id in RBMobileNote.find(creator_set = [int(user_id)]):
            _note_context = RBMobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = RBMobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context, 
                })
            else:
                _rslt.append({
                    'note' : _note_context
                })

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
        for _entity_id in RBMobileEntity.search(_query):
            _rslt.append(RBMobileEntity(_entity_id).read(_request_user_id))
        
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
            else:
                _rslt.append({
                    'type' : 'candidate',
                    'object' : {
                        'note' : _note_context
                    }
                })
        
        return SuccessJsonResponse(_rslt)
