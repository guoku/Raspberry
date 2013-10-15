# coding=utf8
from common.entity import RBEntity
from common.user import RBUser


class RBMobileUser(RBUser):
    
    def __init__(self, user_id):
        RBUser.__init__(self, user_id)
    
    def read(self, request_user_id = None):
        _context = super(RBMobileUser, self).read()
        if request_user_id:
            _context['relation'] = RBMobileUser.get_relation(request_user_id, self.get_user_id())
        return _context
    
    def read_full_context(self, request_user_id = None):
        _context = self.read(request_user_id) 
        
        _context = super(RBMobileUser, self).read()
        if request_user_id:
            _context['relation'] = RBUser.get_relation(request_user_id, self.get_user_id())
            _context['following_count'] = len(self.get_following_user_id_list())
            _context['fan_count'] = len(self.get_fan_user_id_list())
            _context['like_count'] = RBEntity.get_user_like_count(self.get_user_id())
            _context['note_count'] = RBEntity.get_user_note_count(self.get_user_id())
        return _context
