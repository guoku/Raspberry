# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from common.note import RBNote
from user import RBMobileUser
import time


class RBMobileNote(RBNote):
    
    @classmethod
    def create_by_note(cls, note):
        _inst = cls(note.note_id)
        if hasattr(note, 'note_obj'):
            _inst.note_obj = note.note_obj
        if hasattr(note, 'figure_obj'):
            _inst.figure_obj = note.figure_obj
        return _inst
        
    
    def read(self, request_user_id = None):
        _context = super(RBMobileNote, self).read(json = True)
        
        _context['creator'] = RBMobileUser(_context['creator_id']).read(request_user_id)
        del _context['creator_id']
        
        if request_user_id and self.poke_already(request_user_id):
            _context['poke_already'] = 1
        else:
            _context['poke_already'] = 0

        if _context.has_key('entity_id') and _context['entity_id'] != None:
            _entity = RBEntity(_context['entity_id'])
            _entity_context = _entity.read()
            _context['entity_brand'] = _entity_context['brand']
            _context['entity_title'] = _entity_context['title']
            _context['entity_chief_image'] = _entity_context['chief_image']
        return _context 
    
    def read_note_full_context(self, note_id, request_user_id = None):
        _context = {}
        _context['note'] = self.read(request_user_id)
        _context['poker_list'] = []
        for _poker_id in _context['note']['poker_id_list']: 
            _context['poker_list'].append(RBMobileUser(_poker_id).read(request_user_id))
        del _context['note']['poker_id_list']
        _context['comment_list'] = [] 
        for _comment_id in _context['note']['comment_id_list']: 
            _context['comment_list'].append(self.read_comment(_comment_id, json = True))
        del _context['note']['comment_id_list']
        return _context

    def read_comment(self, comment_id, json = False):
        _context = super(RBMobileNote, self).read_comment(comment_id, json = True)
        return _context
