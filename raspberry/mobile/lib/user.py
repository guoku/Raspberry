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
    
