# coding=utf8
from common.item import RBItem
from common.candidate import RBCandidate
from user import RBMobileUser
from note import RBMobileNote
import time


class RBMobileCandidate(RBCandidate):
    
    def __init__(self, candidate_id):
        RBCandidate.__init__(self, candidate_id)

