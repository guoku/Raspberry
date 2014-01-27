# coding=utf8
from django.conf import settings
from base.stream_models import TaobaoShop as TaobaoShopModel
from base.stream_models import TaobaoShopInfo
from base.stream_models import TaobaoShopExtendedInfo
from base.stream_models import CrawlerInfo
from base.stream_models import TaobaoShopVerificationInfo
from base.stream_models import GuokuPlusApplication
import datetime
import urllib
import pymongo

class TaobaoShop(object):
    
    def __init__(self, nick):
        self.nick = nick 
   
    @staticmethod
    def nick_exist(nick):
        return TaobaoShopModel.objects.filter(shop_info__nick = nick).count() > 0

    @staticmethod
    def find(nick, offset, num, sort_by, contained_gifts):
        if nick:
            _hdl = TaobaoShopModel.objects(shop_info__nick = nick)
        else:
            _hdl = TaobaoShopModel.objects
        if contained_gifts:
            _hdl = _hdl.filter(extended_info__gifts__in=contained_gifts)
        count = _hdl.count()
        if sort_by:
            _hdl = _hdl.order_by(sort_by)
        results = _hdl.skip(offset).limit(num)
        return results, count
        
    @classmethod
    def create(cls, nick, shop_id, title, shop_type, seller_id, pic_path):
        _now = datetime.datetime.now()
        shop = TaobaoShopModel(
            shop_info = TaobaoShopInfo(
                sid = int(shop_id),
                nick = nick, 
                title = title,
                shop_type = shop_type,
                seller_id = int(seller_id),
                pic_path = pic_path,
                shop_score = ShopScore(credit = "", praise_rate = 0),
                main_products = "",
                location = ""
            ),
            extended_info = TaobaoShopExtendedInfo(
                orientational = False,
                commission_rate = -1
            ),
            crawler_info = CrawlerInfo(priority = 10, cycle = 720),
            created_time = _now,
            last_updated_time = _now
        )
        shop.save()
        _inst = cls(nick)
        return _inst 


    def read(self, full_info = False):
        _hdl = TaobaoShopModel.objects.filter(shop_info__nick = self.nick)
        if _hdl.count() == 0:
            return None
        _doc = _hdl.first()
        print _doc.crawler_info._data
        _context = {}
        _context['shop_nick'] = self.nick
        _context['shop_id'] = _doc.shop_info.sid
        _context['title'] = _doc.shop_info.title
        _context['shop_type'] = _doc.shop_info.shop_type 
        _context['seller_id'] = _doc.shop_info.seller_id 
        '''
        _context['commission_rate'] = -1
        _context['commission_type'] = 'unknown' 
        if _doc.extended_info:
            if _doc.extended_info.orientational:
                _context['commission_type'] = 'orientational'
                _context['commission_rate'] = _doc.extended_info.commission_rate
            elif _doc.extended_info.commission_rate != -1:
                _context['commission_type'] = 'general'
                _context['commission_rate'] = _doc.extended_info.commission_rate
        if full_info:
            _context
        '''

        _context['extended_info'] = _doc.extended_info._data
        _context['crawler_info'] = _doc.crawler_info._data
        if _doc.shop_info.shop_score:
            _context['shop_score'] = _doc.shop_info.shop_score._data
        
        return _context
   
    STATUS_WAITING = 'waiting'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    def update(self, priority = None, cycle = None, shop_type = None,
               orientational = None, commission = None, commission_rate = None,
               original = None, gifts = None, main_products = None, single_tail = None):
        shop = TaobaoShopModel.objects.filter(shop_info__nick = self.nick).first()
        if shop:
            if priority:
                shop.crawler_info.priority = priority
            if cycle:
                shop.crawler_info.cycle = cycle
            if shop_type:
                shop.shop_info.shop_type = shop_type
            if orientational:
                shop.extended_info.orientational = orientational
            if commission:
                shop.extended_info.commission = commission
            if commission_rate:
                shop.extended_info.commission_rate = commission_rate
            if gifts:
                shop.extended_info.gifts = gifts
            if main_products:
                shop.extended_info.main_products = main_products
            if single_tail:
                shop.extended_info.single_tail = single_tail
            shop.save()

    def create_verification_info(self, intro):
        info = TaobaoShopVerificationInfo(
            shop_nick = self.nick,
            intro = intro,
            status = STATUS_WAITING,
            created_time = datetime.datetime.now()
            )
        info.save()

    def create_guoku_plus_application(self, taobao_item_id, quantity, original_price, sale_price, duration):
        item = GuokuPlusApplication(
            shop_nick = self.nick,
            taobao_item_id = taobao_item_id,
            quantity = quantity,
            original_price = original_price,
            sale_price = sale_price,
            duration = duration,
            status = STATUS_WAITING,
            created_time = datetime.datetime.now()
            )
        item.save()
