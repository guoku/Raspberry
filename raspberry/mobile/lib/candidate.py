# coding=utf8
from common.item import RBItem
from common.candidate import RBCandidate
from user import RBMobileUser
from note import RBMobileNote
import time


class RBMobileCandidate(RBCandidate):
    
    def __init__(self, candidate_id):
        RBCandidate.__init__(self, candidate_id)

    def read(self, request_user_id = None):
        _context = {}
        _context['candidate'] = super(RBMobileCandidate, self).read(json = True)
        _context['note'] = RBMobileNote(_context['candidate']['note_id']).read(request_user_id) 

        return _context
    
