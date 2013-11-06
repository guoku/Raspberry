# coding=utf8
from common.candidate import RBCandidate
from common.entity import RBEntity
from common.user import User


class RBMobileUser(User):
    
    def __init__(self, user_id):
        User.__init__(self, user_id)
    
    def read(self, request_user_id = None):
        _context = super(RBMobileUser, self).read()
        if request_user_id:
            _context['relation'] = RBMobileUser.get_relation(request_user_id, self.user_id)
        return _context
    
    def read_full_context(self, request_user_id = None):
        _context = self.read(request_user_id) 
        
        _context = super(RBMobileUser, self).read()
        _context['following_count'] = len(self.get_following_user_id_list())
        _context['fan_count'] = len(self.get_fan_user_id_list())
        _context['like_count'] = RBEntity.get_user_like_count(self.user_id)
        _context['entity_note_count'] = RBEntity.get_user_entity_note_count(self.user_id)
        _context['share_count'] = RBCandidate.count(creator_id = self.user_id)
        if request_user_id:
            _context['relation'] = User.get_relation(request_user_id, self.user_id)
        return _context
