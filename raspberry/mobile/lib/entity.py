# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from user import RBMobileUser
from note import RBMobileNote
import time

class RBMobileItem(RBItem):

    def __init__(self, item_id):
        RBItem.__init__(self, item_id)

    def read(self):
        _context = super(RBMobileItem, self).read()
        return _context


class RBMobileEntity(RBEntity):
    
    def __init__(self, entity_id):
        RBEntity.__init__(self, entity_id)

    def read(self, request_user_id = None):
        _context = super(RBMobileEntity, self).read(json = True)

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
            _request_user_note_id_list = RBEntity.find_entity_note(entity_id = self.entity_id, creator_id = request_user_id)
            if _request_user_note_id_list != None and len(_request_user_note_id_list) > 0:
                _context['my_note'] = RBMobileNote(_request_user_note_id_list[0]['note_id']).read(request_user_id) 
        
        return _context
    
    def read_full_context(self, request_user_id = None):
        _context = {}
        _context['entity'] = self.read(request_user_id) 
        
        _context['entity']['item_list'] = []
        for _item_id in _context['entity']['item_id_list']:
            _context['entity']['item_list'].append(RBMobileItem(_item_id).read())
        del _context['entity']['item_id_list']

        _context['note_list'] = []
        for _note_id in _context['entity']['note_id_list']:
            _context['note_list'].append(RBMobileNote(_note_id).read(request_user_id)) 
        del _context['entity']['note_id_list']
     
        if request_user_id:
            _context['following_note_list'] = []
            for _followee_id in RBMobileUser(request_user_id).get_following_user_id_list():
                _context['following_note_list'].append(RBMobileUser(_followee_id).read())
        
        return _context    
    
    def add_note(self, creator_id, score, note_text, image_data):
        _note_origin = super(RBMobileEntity, self).add_note(creator_id, score, note_text, image_data)
        _note = RBMobileNote.create_by_note(_note_origin)
        return _note
    
    def update_note(self, note_id, score, note_text, image_data):
        _note_origin = super(RBMobileEntity, self).update_note(note_id, score, note_text, image_data)
        _note = RBMobileNote.create_by_note(_note_origin)
        return _note
        

