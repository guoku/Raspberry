# coding=utf8
from common.item import RBItem
from common.entity import RBEntity
from user import RBMobileUser
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
        _context = super(RBMobileEntity, self).read()
        _context['created_time'] = time.mktime(_context["created_time"].timetuple())
        _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        
        _context['like_already'] = 0
        if request_user_id: 
            if self.like_already(request_user_id):
                _context['like_already'] = 1
            _note_id = self.get_user_note(request_user_id)
            if _note_id != None:
                _context['my_note'] = self.read_note(_note_id, request_user_id) 
        
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
            _context['note_list'].append(self.read_note(_note_id, request_user_id)) 
        del _context['entity']['note_id_list']
     
        if request_user_id:
            _context['following_note_list'] = []
            for _followee_id in RBMobileUser(request_user_id).get_following_user_id_list():
                _context['following_note_list'].append(RBMobileUser(_followee_id).read())
        
        return _context    


    def add_note(self, creator_id, score, note_text, request_user_id = None):
        _note_context = super(RBMobileEntity, self).add_note(creator_id, score, note_text)
        _note_context['creator'] = RBMobileUser(_note_context['creator_id']).read(request_user_id)
        del _note_context['creator_id']
        _note_context['created_time'] = time.mktime(_note_context["created_time"].timetuple())
        _note_context['updated_time'] = time.mktime(_note_context["updated_time"].timetuple())
        _note_context['poke_already'] = 0
        return _note_context
    
    def read_note(self, note_id, request_user_id = None):
        _entity_context = super(RBMobileEntity, self).read()
        
        _note_context = super(RBMobileEntity, self).read_note(note_id)
        _note_context['entity_chief_image'] = _entity_context['chief_image']
        _note_context['creator'] = RBMobileUser(_note_context['creator_id']).read(request_user_id)
        _note_context['creator_like_already'] = self.like_already(_note_context['creator_id'])
        del _note_context['creator_id']
        _note_context['created_time'] = time.mktime(_note_context["created_time"].timetuple())
        _note_context['updated_time'] = time.mktime(_note_context["updated_time"].timetuple())
        if request_user_id and self.poke_note_already(note_id, request_user_id):
            _note_context['poke_already'] = 1
        else:
            _note_context['poke_already'] = 0
        return _note_context 
    
    def read_note_full_context(self, note_id, request_user_id = None):
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

    def add_note_comment(self, note_id, comment_text, creator_id, reply_to, request_user_id = None):
        _comment_context = super(RBMobileEntity, self).add_note_comment(
            note_id = note_id,
            comment_text = comment_text,
            creator_id = creator_id,
            reply_to = reply_to
        )
        _comment_context['creator'] = RBMobileUser(_comment_context['creator_id']).read(request_user_id)
        del _comment_context['creator_id']
        _comment_context['created_time'] = time.mktime(_comment_context["created_time"].timetuple())
        return _comment_context
    
    def read_note_comment(self, note_id, comment_id, request_user_id = None):
        _comment_context = super(RBMobileEntity, self).read_note_comment(note_id, comment_id)
        _comment_context['creator'] = RBMobileUser(_comment_context['creator_id']).read(request_user_id)
        del _comment_context['creator_id']
        _comment_context['created_time'] = time.mktime(_comment_context["created_time"].timetuple())
        return _comment_context
