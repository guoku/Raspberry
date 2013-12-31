# coding=utf8
from django.conf import settings
from models import Item as ItemDocument
from models import TaobaoItem as TaobaoItemDocument
import datetime
import urllib

class Item(object):
    
    def __init__(self, item_id):
        self.item_id = item_id
    
    def __ensure_item_obj(self):
        if not hasattr(self, 'item_obj'):
            self.item_obj = ItemDocument.objects.filter(id = self.item_id).first()
    
    def get_entity_id(self):
        self.__ensure_item_obj()
        return self.item_obj.entity_id
    
    @classmethod
    def create_taobao_item(cls, entity_id, images, taobao_id, cid, title, shop_nick, price, soldout): 
        _taobao_id = taobao_id.strip()
        _title = title.strip()
        _shop_nick = shop_nick.strip()
        
        _item_obj = TaobaoItemDocument( 
            entity_id = entity_id,
            images = images,
            source = 'taobao',
            taobao_id = _taobao_id,
            cid = cid,
            title = _title,
            shop_nick = _shop_nick,
            price = price,
            soldout = soldout,
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        _item_obj.save()

        _inst = cls(_item_obj.id)
        _inst.item_obj = _item_obj
        return _inst

    
    def __load_taobao_item(self):
        _context = {}
        _context["item_id"] = str(self.item_obj.id)
        _context["entity_id"] = self.item_obj.entity_id
        _context["source"] = self.item_obj.source
        _context["taobao_id"] = self.item_obj.taobao_id
        _context["cid"] = self.item_obj.cid
        _context["title"] = self.item_obj.title
        _context["shop_nick"] = self.item_obj.shop_nick
        _context["price"] = float(self.item_obj.price)
        _context["soldout"] = self.item_obj.soldout
        _context['buy_link'] = Item.generate_taobao_item_url(_context['taobao_id'])
        _context["volume"] = 0 
        return _context

    def read(self):
        self.__ensure_item_obj()
        if self.item_obj.source == 'taobao':
            _context = self.__load_taobao_item()
        return _context
    
    @classmethod
    def find(cls, entity_id = None, offset = 0, count = 30, full_info = False):
        _hdl = ItemDocument.objects.all()
        if entity_id != None:
            _entity_id = int(entity_id)
            _hdl = _hdl.filter(entity_id = _entity_id)
        _item_list = []
        for _doc in _hdl.order_by('-created_time')[offset : offset + count]:
            if full_info:
                _item_list.append({
                    'item_id' : str(_doc.id),
                    'taobao_id' : _doc.taobao_id,
                    'entity_id' : _doc.entity_id,
                })
            else:
                _item_list.append(str(_doc.id))
        return _item_list

    
    def bind(self, entity_id):
        self.__ensure_item_obj()
        self.item_obj.entity_id = entity_id 
        self.item_obj.save()
    
    @classmethod
    def get_item_by_taobao_id(cls, taobao_id):
        _taobao_item_obj = TaobaoItemDocument.objects.filter(taobao_id = taobao_id).first()
        if _taobao_item_obj != None:
            _inst = cls(str(_taobao_item_obj.id))
            _inst.item_obj = _taobao_item_obj
            return _inst 
        return None
    
    @staticmethod
    def generate_taobao_item_url(taobao_id):
        _url = settings.APP_HOST + "/visit_item?item_id=%s" % taobao_id + "&type=mobile"
        return _url

    @staticmethod
    def get_item_id_list_by_entity_id(entity_id):
        _list = []
        for _item in ItemDocument.objects.filter(entity_id = entity_id):
            _list.append(str(_item.id))
        return _list
