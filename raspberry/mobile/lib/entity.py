# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from user import RBMobileUser
from note import RBMobileNote
import time

class RBMobileItem(RBItem):

    def __init__(self, item_id):
        RBItem.__init__(self, item_id)

    @staticmethod
    def generate_taobao_item_url(taobao_id):
        return 'http://item.taobao.com/item.htm?id=' + taobao_id

    def read(self):
        _context = super(RBMobileItem, self).read()
        _context['buy_link'] = RBMobileItem.generate_taobao_item_url(_context['taobao_id'])
        return _context


class RBMobileEntity(RBEntity):
    
    def __init__(self, entity_id):
        RBEntity.__init__(self, entity_id)

    def read(self, request_user_id = None):
        _context = super(RBMobileEntity, self).read(json = True)
        
        _context['like_already'] = 0
        if request_user_id: 
            if self.like_already(request_user_id):
                _context['like_already'] = 1
            _request_user_note_id = self.get_entity_note_of_user(request_user_id)
            if _note_id != None:
                _context['my_note'] = RBMobileNote(_note_id).read(request_user_id) 
        
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
            _context['note_list'].append(RBMobileNote(_note_id).read_note(request_user_id)) 
        del _context['entity']['note_id_list']
     
        if request_user_id:
            _context['following_note_list'] = []
            for _followee_id in RBMobileUser(request_user_id).get_following_user_id_list():
                _context['following_note_list'].append(RBMobileUser(_followee_id).read())
        
        return _context    

