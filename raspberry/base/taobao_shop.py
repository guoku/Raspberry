# coding=utf8
from django.conf import settings
from base.stream_models import TaobaoShop as TaobaoShopModel
import datetime
import urllib
import pymongo

class TaobaoShop(object):
    
    def __init__(self, nick):
        self.nick = nick 
   
    @staticmethod
    def nick_exist(nick):
        return TaobaoShopModel.objects.filter(shop_info__nick = nick).count() > 0

    @classmethod
    def create(cls, nick, shop_id, title, shop_type, seller_id, pic_path):
        shop = TaobaoShopModel(
            shop_info = TaobaoShopInfo(
                sid = int(shop_id),
                nick = nick, 
                title = title,
                shop_type = shop_type,
                seller_id = int(seller_id),
                pic_path = pic_path
            )
        )
        shop.save()
        _inst = cls(nick)
        return _inst 


    def read(self):
        _hdl = TaobaoShopModel.objects.filter(shop_info__nick = self.nick)
        if _hdl.count() == 0:
            return None
        _doc = _hdl.first()
        _context = {}
        _context['shop_nick'] = self.nick
        _context['shop_id'] = _doc.shop_info.sid
        _context['title'] = _doc.shop_info.title
        _context['shop_type'] = _doc.shop_info.shop_type 
        _context['seller_id'] = _doc.shop_info.seller_id 
        _context['commission_rate'] = -1
        _context['commission_type'] = 'unknown' 
        if _doc.extended_info:
            if _doc.extended_info.orientational:
                _context['commission_type'] = 'orientational'
                _context['commission_rate'] = _doc.extended_info.commission_rate
            elif _doc.extended_info.commission_rate != -1:
                _context['commission_type'] = 'general'
                _context['commission_rate'] = _doc.extended_info.commission_rate

        return _context
    
