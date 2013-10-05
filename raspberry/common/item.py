# coding=utf8
import urllib
from mango.client import MangoApiClient

class RBItem(object):
    
    def __init__(self, item_id):
        self.__item_id = int(item_id)
    
    @classmethod
    def read_items(cls, item_id_list):
        _mango_client = MangoApiClient()
        
        _context_list = []
        for _item_id in item_id_list:
            _context = _mango_client.read_item(_item_id)
            _context_list.append(_context)
        return _context_list
             
