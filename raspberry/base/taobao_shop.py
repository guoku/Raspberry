# coding=utf8
from django.conf import settings
from models import Item as ItemDocument
from models import TaobaoItem as TaobaoItemDocument
import datetime
import urllib
import pymongo


HOST = getattr(settings, 'MANGO_HOST', 'localhost')
PORT = getattr(settings, 'MANGO_PORT', 27017)

class TaobaoShop(object):
    
    def __init__(self, nick):
        self.nick = nick 
        self.client = pymongo.Connection(HOST, PORT)
        self.db = self.client['mango']
        self.shop_coll = self.db['taobao_shops_depot']
   
    @staticmethod
    def nick_exist(nick):
        _client = pymongo.Connection(HOST, PORT)
        _db = _client['guoku']
        _coll = _db['taobao_shop']
        
        _count = _coll.find({'shop_info.nick' : nick }).count()
        if _count == 0:
            return False
        return True


    @classmethod
    def create(cls, nick, shop_id, title, shop_type, seller_id, pic_path):
        _client = pymongo.Connection(HOST, PORT)
        _db = _client['guoku']
        _coll = _db['taobao_shop']
        
        _doc = {
            'shop_info' : {
                'sid' : int(shop_id),
                'nick' : nick, 
                'title' : title,
                'shop_type' : shop_type,
                'seller_id' : int(seller_id),
                'pic_path' : pic_path 
            }
        }
        _coll.insert(_doc)
        _inst = cls(nick)
        return _inst 


    def read(self):
        
        _hdl = self.shop_coll.find({'shop_info.nick' : self.nick })
        
        if _hdl.count() == 0:
            return None
        _doc = _hdl[0]
        
        _context = {}
        _context['shop_nick'] = self.nick
        _context['shop_id'] = _doc['shop_info']['sid']
        _context['title'] = _doc['shop_info']['title']
        #_context['shop_type'] = _doc['shop_info']['shop_type'] 
        #_context['seller_id'] = _doc['shop_info']['seller_id'] 
        _context['commission_rate'] = -1
        _context['commission_type'] = 'unknown' 
        if _doc.has_key('extended_info'):
            if _doc['extended_info']['orientational']:
                _context['commission_type'] = 'orientational'
                _context['commission_rate'] = _doc['extended_info']['commission_rate']
            elif _doc['extended_info']['commission_rate'] != -1:
                _context['commission_type'] = 'general'
                _context['commission_rate'] = _doc['extended_info']['commission_rate']

        return _context
    
