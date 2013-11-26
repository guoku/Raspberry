# coding=utf8
from base.entity import Entity
from base.note import Note 
from base.user import User


class MobileUser(User):
    
    def __init__(self, user_id):
        User.__init__(self, user_id)
    
    def read(self, request_user_id = None):
        _context = super(MobileUser, self).read()
        if request_user_id:
            _context['relation'] = MobileUser.get_relation(request_user_id, self.user_id)
        return _context
    
    def read_full_context(self, request_user_id = None):
        _context = self.read(request_user_id) 
        
        _context = super(MobileUser, self).read()
        _context['following_count'] = self.get_following_count()
        _context['fan_count'] = self.get_fan_count()
        _context['like_count'] = Entity.get_user_like_count(self.user_id)
        _context['entity_note_count'] = Note.count(creator_set = [self.user_id])
        if request_user_id:
            _context['relation'] = User.get_relation(request_user_id, self.user_id)
        return _context
