# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from user import RBMobileUser
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 
import time

class RBMobileItem(RBItem):

    def __init__(self, item_id):
        RBItem.__init__(self, item_id)

    def read(self):
        _context = super(RBMobileItem, self).read()
        return _context


class RBMobileEntity(RBEntity):
    
    def __init__(self, entity_id):
        RBEntity.__init__(self, entity_id)

    def read(self, user_id):
        _context = super(RBMobileEntity, self).read()
        _context['created_time'] = time.mktime(_context["created_time"].timetuple())
        _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        
        if user_id and self.like_already(user_id):
            _context['like_already'] = 1
        else:
            _context['like_already'] = 0
        
        return _context
    
    def read_full_context(self, user_id):
        _context = self.read(user_id) 
        
        _context['item_list'] = []
        for _item_id in _context['item_id_list']:
            _context['item_list'].append(RBMobileItem(_item_id).read())
        del _context['item_id_list']

        _context['note_list'] = []
        for _note_id in _context['note_id_list']:
            _context['note_list'].append(self.read_note(_note_id, user_id)) 
        del _context['note_id_list']
       
        _context['note_friend_list'] = []
        for _followee_id in RBMobileUser(user_id).get_following_user_id_list():
            _context['note_friend_list'].append(RBMobileUser(_followee_id).read())
        
        return _context    

    def add_note(self, creator_id, note_text):
        _note_context = super(RBMobileEntity, self).add_note(creator_id, note_text)
        _note_context['created_time'] = time.mktime(_note_context["created_time"].timetuple())
        _note_context['updated_time'] = time.mktime(_note_context["updated_time"].timetuple())
        return _note_context
    
    def read_note(self, note_id, user_id):
        _note_context = super(RBMobileEntity, self).read_note(note_id)
        _note_context['created_time'] = time.mktime(_note_context["created_time"].timetuple())
        _note_context['updated_time'] = time.mktime(_note_context["updated_time"].timetuple())
        if user_id and self.poke_note_already(note_id, user_id):
            _note_context['poke_already'] = 1
        else:
            _note_context['poke_already'] = 0
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
