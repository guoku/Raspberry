# coding=utf8
import urllib
from utils.mango_client import MangoApiClient

class RBItem(object):
    
    def __init__(self, item_id):
        self.__item_id = int(item_id)
    
    @classmethod
    def read_items(cls, item_id_list):
        _mango_client = MangoApiClient()
        _base_datum = _mango_client.read_items(item_id_list)
        
        _context_list = []
        for _item_id in item_id_list:
            if _base_datum.has_key(str(_item_id)):
                if _base_datum[str(_item_id)]['status'] == '0':
                    _context_list.append(_base_datum[str(_item_id)]['context'])
        return _context_list
             
