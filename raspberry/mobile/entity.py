# coding=utf8
from common.entity import RBEntity
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 
import time


class RBMobileEntity(RBEntity):
    
    def __init__(self, entity_id):
        RBEntity.__init__(self, entity_id)

    def read(self):
        _context = super(RBMobileEntity, self).read()
        _context['created_time'] = time.mktime(_context["created_time"].timetuple())
        _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        return _context

    def add_note(self, creator_id, note_text):
        _note_context = super(RBMobileEntity, self).add_note(creator_id, note_text)
        _note_context['created_time'] = time.mktime(_note_context["created_time"].timetuple())
        _note_context['updated_time'] = time.mktime(_note_context["updated_time"].timetuple())
        return _note_context
    


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

