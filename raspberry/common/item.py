# coding=utf8
import urllib
from mango.client import MangoApiClient

class RBItem(object):
    
    def __init__(self, item_id):
        self.__item_id = item_id
    
    def read(self):
        _mango_client = MangoApiClient()
        _context = _mango_client.read_item(self.__item_id)
        _context['buy_link'] = RBItem.generate_taobao_item_url(_context['taobao_id'])
        return _context
    
    @staticmethod
    def get_item_id_by_taobao_id(taobao_id):
        _mango_client = MangoApiClient()
        return _mango_client.get_item_id_by_taobao_id(taobao_id)
    
    @staticmethod
    def generate_taobao_item_url(taobao_id):
        return 'http://item.taobao.com/item.htm?id=' + taobao_id

