# coding=utf8
from common.item import Item
from common.entity import Entity
from common.note import Note
from user import MobileUser
import time


class MobileNote(Note):
    
    @classmethod
    def create_by_note(cls, note):
        _inst = cls(note.note_id)
        if hasattr(note, 'note_obj'):
            _inst.note_obj = note.note_obj
        if hasattr(note, 'figure_obj'):
            _inst.figure_obj = note.figure_obj
        return _inst
        
    
    def read(self, request_user_id = None):
        _context = super(MobileNote, self).read(json = True)
        
        _context['creator'] = MobileUser(_context['creator_id']).read(request_user_id)
        del _context['creator_id']
        
        if request_user_id and self.poke_already(request_user_id):
            _context['poke_already'] = 1
        else:
            _context['poke_already'] = 0

        if _context.has_key('entity_id') and _context['entity_id'] != None:
            _entity = Entity(_context['entity_id'])
            _entity_context = _entity.read()
            _context['brand'] = _entity_context['brand']
            _context['title'] = _entity_context['title']
            _context['chief_image'] = _entity_context['chief_image']
            _context['category_id'] = _entity_context['category_id']
            
        return _context 
    
    def read_note_full_context(self, request_user_id = None):
        _context = {}
        _context['note'] = self.read(request_user_id)
        _context['poker_list'] = []
        for _poker_id in _context['note']['poker_id_list']: 
            _context['poker_list'].append(MobileUser(_poker_id).read(request_user_id))
        del _context['note']['poker_id_list']
        _context['comment_list'] = [] 
        for _comment_id in _context['note']['comment_id_list']: 
            _comment_context = self.read_comment(_comment_id, request_user_id) 
            _context['comment_list'].append(_comment_context)
        del _context['note']['comment_id_list']
        return _context

    def read_comment(self, comment_id, request_user_id = None):
        _context = super(MobileNote, self).read_comment(comment_id, json = True)
        _context['creator'] = MobileUser(_context['creator_id']).read(request_user_id)
        del _context['creator_id']
        if _context.has_key('reply_to_user_id'):
            _context['reply_to_user'] = MobileUser(_context['reply_to_user_id']).read(request_user_id)
            del _context['reply_to_user_id']
            
        return _context
