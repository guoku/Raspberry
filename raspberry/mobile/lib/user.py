# coding=utf8
from common.user import RBUser


class RBMobileUser(RBUser):
    
    def __init__(self, user_id):
        RBUser.__init__(self, user_id)

