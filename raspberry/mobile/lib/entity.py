# coding=utf8
from base.item import Item
from base.entity import Entity
from note import MobileNote
import time

class MobileItem(Item):

    def __init__(self, item_id):
        Item.__init__(self, item_id)

    def read(self):
        _context = super(MobileItem, self).read()
        return _context


class MobileEntity(Entity):
    
    def __init__(self, entity_id):
        Entity.__init__(self, entity_id)

    def read(self, request_user_id = None):
        _context = super(MobileEntity, self).read(json = True)

        _context['chief_image'] = _context['chief_image']['url']
        if _context.has_key('detail_images'):
            _detail_images_clean = []
            for image in _context['detail_images']:
                _detail_images_clean.append(image['url'])
            _context['detail_images'] = _detail_images_clean
            
            
        
        _context['like_already'] = 0
        if request_user_id: 
            if self.like_already(request_user_id):
                _context['like_already'] = 1
            _request_user_note_id_list = MobileNote.find(entity_id = self.entity_id, creator_set = [request_user_id])
            if _request_user_note_id_list != None and len(_request_user_note_id_list) > 0:
                _context['my_note'] = MobileNote(_request_user_note_id_list[0]).read(request_user_id) 
        
        return _context
    
    def read_full_context(self, request_user_id = None):
        _context = {}
        _context['entity'] = self.read(request_user_id) 
        
        _context['entity']['item_list'] = []
        for _item_id in _context['entity']['item_id_list']:
            _context['entity']['item_list'].append(MobileItem(_item_id).read())
        del _context['entity']['item_id_list']
    
        _context['note_list'] = []
        for _note_id in _context['entity']['note_id_list']:
            _context['note_list'].append(MobileNote(_note_id).read(request_user_id)) 
        del _context['entity']['note_id_list']
     
        return _context    
    
    def add_note(self, creator_id, note_text, score = 0, image_data = None):
        _note = super(MobileEntity, self).add_note(
            creator_id = creator_id,
            note_text = note_text,
            score = score,
            image_data = image_data
        )
        _note = MobileNote.create_by_note(_note)
        return _note
