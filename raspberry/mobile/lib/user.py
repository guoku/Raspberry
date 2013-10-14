# coding=utf8
from common.user import RBUser


class RBMobileUser(RBUser):
    
    def __init__(self, user_id):
        RBUser.__init__(self, user_id)
    
    def read(self, request_user_id = None):
        _context = super(RBMobileUser, self).read()
        if request_user_id:
            _context['relation'] = RBMobileUser.get_relation(request_user_id, self.get_user_id())
        return _context
