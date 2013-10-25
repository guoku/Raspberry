# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from common.note import RBNote
from user import RBMobileUser
import time


class RBMobileNote(RBNote):
    
    def read_note(self, note_id, request_user_id = None):
        _context = super(RBMobileNote, self).read(json = True)
        
        _context['creator'] = RBMobileUser(_context['creator_id']).read(request_user_id)
        del _context['creator_id']
        
        if request_user_id and self.poke_already(note_id, request_user_id):
            _context['poke_already'] = 1
        else:
            _context['poke_already'] = 0
        return _context 
    
    def read_note_full_context(self, note_id, request_user_id = None):
        _entity_context = super(RBMobileEntity, self).read()
        
        _context = {}
        _context['note'] = self.read_note(note_id, request_user_id)
        _context['entity'] = self.read(request_user_id)
        _context['poker_list'] = []
        for _poker_id in _context['note']['poker_id_list']: 
            _context['poker_list'].append(RBMobileUser(_poker_id).read(request_user_id))
        del _context['note']['poker_id_list']
        _context['comment_list'] = [] 
        for _comment_id in _context['note']['comment_id_list']: 
            _context['comment_list'].append(self.read_note_comment(note_id, _comment_id, request_user_id))
        del _context['note']['comment_id_list']
        return _context

    def read_comment(self, comment_id, request_user_id = None):
        _comment_context = super(RBMobileNote, self).read_comment(comment_id)
        _comment_context['creator'] = RBMobileUser(_comment_context['creator_id']).read(request_user_id)
        del _comment_context['creator_id']
        _comment_context['created_time'] = time.mktime(_comment_context["created_time"].timetuple())
        return _comment_context
