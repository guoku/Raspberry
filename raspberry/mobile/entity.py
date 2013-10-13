# coding=utf8
from lib.entity import RBMobileEntity
from lib.user import RBMobileUser
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 

def category_entity(request, category_id):
    _entity_id_list = RBEntity.find(
        category_id = category_id
    )
    _rslt = []
    for _entity_id in _entity_id_list:
        _entity = RBMobileEntity(_entity_id)
        _rslt.append(
            _entity.read()
        )
        
    return SuccessJsonResponse(_rslt)


def entity_detail(request, entity_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _user_id = Session_Key.objects.get_user_id(_session)
        else:
            _user_id = None

        _rslt = RBMobileEntity(entity_id).read_full_context(_user_id)
        return SuccessJsonResponse(_rslt)
        


def like_entity(request, entity_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 'entity_id' : entity_id }
        if target_status == '1':
            RBMobileEntity(entity_id).like(_user_id)
            _rslt['like_already'] = 1
        else:
            RBMobileEntity(entity_id).unlike(_user_id)
            _rslt['like_already'] = 0
        return SuccessJsonResponse(_rslt)
            

def add_note_for_entity(request, entity_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _note_text = request.POST.get('note', None)
        
        _user_id = Session_Key.objects.get_user_id(_session)
        _entity = RBMobileEntity(entity_id)
        _note_context = _entity.add_note(
            creator_id = _user_id,
            note_text = _note_text
        )
        return SuccessJsonResponse(_note_context)

def entity_note_detail(request, entity_id, note_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _user_id = Session_Key.objects.get_user_id(_session)
        else:
            _user_id = None

        _rslt = RBMobileEntity(entity_id).read_note_full_context(note_id, _user_id)
        return SuccessJsonResponse(_rslt)

def poke_entity_note(request, entity_id, note_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 
            'entity_id' : entity_id, 
            'note_id' : note_id 
        }
        if target_status == '1':
            RBMobileEntity(entity_id).poke_note(note_id, _user_id)
            _rslt['poke_already'] = 1
        else:
            RBMobileEntity(entity_id).depoke_note(note_id, _user_id)
            _rslt['poke_already'] = 0
        return SuccessJsonResponse(_rslt)

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
        for _note_info in RBMobileEntity.note_list_of_user(user_id):
            _entity_id = _note_info['entity_id'] 
            _note_id = _note_info['note_id']
            _entity = RBMobileEntity(_entity_id)
            _rslt.append({
                'entity' : _entity.read(_request_user_id),
                'note' : _entity.read_note(_note_id, _request_user_id)
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
