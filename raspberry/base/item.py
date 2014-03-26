# coding=utf8
from django.conf import settings
from django.core.cache import cache
from models import Item as ItemDocument
from models import TaobaoItem as TaobaoItemDocument
from models import JDItem as JDItemDocument
from utils.lib import roll
from utils.jd import get_jd_url
import datetime
import pymongo
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
    def create_taobao_item(cls, entity_id, images, taobao_id, cid, title, shop_nick, price, soldout, weight=0): 
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
            weight = weight,
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        _item_obj.save() 
        _inst = cls(_item_obj.id)
        _inst.item_obj = _item_obj
        return _inst
    
    def update(self, cid = None, title = None, shop_nick = None, price = None, soldout = None, ustation = None, weight = None):
        self.__ensure_item_obj()
        if cid != None:
            self.item_obj.cid = int(cid)
        if title != None:
            self.item_obj.title = title
        if shop_nick != None:
            self.item_obj.shop_nick = shop_nick
        if price != None:
            self.item_obj.price = float(price)
        if soldout != None:
            self.item_obj.soldout = soldout
        if ustation != None:
            self.item_obj.ustation = ustation
        if weight != None:
            self.item_obj.weight = weight
        self.item_obj.updated_time = datetime.datetime.now()
        self.item_obj.save()
       
        
        ## CLEAN_OLD_CACHE ## 
        cache.delete("entity_context_%s"%self.item_obj.entity_id)

    
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
        _context["weight"] = self.item_obj.weight
        _context["soldout"] = self.item_obj.soldout
        _context["ustation"] = self.item_obj.ustation
        _context['buy_link'] = Item.generate_old_buy_link(str(self.item_obj.taobao_id))
        _context["volume"] = 0 
        return _context

    def read(self):
        self.__ensure_item_obj()
        if self.item_obj.source == 'taobao':
            _context = self.__load_taobao_item()
            return _context
        else:
            return None #jd item
    
    @classmethod
    def find_ustation(cls):
        _list = []
        for _doc in TaobaoItemDocument.objects.filter(ustation = 0):
            _list.append({
                'item_id' : str(_doc.id),
                'taobao_id' : _doc.taobao_id,
                'entity_id' : _doc.entity_id,
            })
        return _list

    
    @classmethod
    def find(cls, entity_id = None, offset = 0, count = 30, full_info = False):
        _hdl = ItemDocument.objects.all()
        if entity_id != None:
            _entity_id = int(entity_id)
            _hdl = _hdl.filter(entity_id = _entity_id)
        _item_list = []
        for _doc in _hdl.order_by('-weight', '-created_time')[offset : offset + count]:
            if full_info:
                _item_list.append({
                    'item_id' : str(_doc.id),
                    'taobao_id' : _doc.taobao_id,
                    'entity_id' : _doc.entity_id,
                })
            else:
                _item_list.append(str(_doc.id))
        return _item_list

    @classmethod
    def find_taobao_item(cls, entity_id=None, shop_nick=None, offset=0, count=30, full_info=False, order_by=None):
        _hdl = TaobaoItemDocument.objects.all()
        if entity_id != None:
            _entity_id = int(entity_id)
            _hdl = _hdl.filter(entity_id = _entity_id)
        if shop_nick != None:
            _hdl = _hdl.filter(shop_nick = shop_nick)
        _hdl = _hdl.order_by('-created_time')
            
        _item_list = []
        for _doc in _hdl[offset : offset + count]:
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
    def generate_buy_link(item_id):
        _url = settings.APP_HOST + "/mobile/v3/item/%s/visit/"%item_id + "?type=mobile"
        return _url
    
    @staticmethod
    def generate_old_buy_link(taobao_id):
        _url = settings.APP_HOST + "/visit_item?item_id=%s"%taobao_id + "&type=mobile"
        return _url


class JDItem(Item):
    
    def __ensure_item_obj(self):
        if not hasattr(self, 'item_obj'):
            self.item_obj = JDItemDocument.objects.filter(id = self.item_id).first()


    @classmethod
    def get_item_by_jd_id(cls, jd_id):
        _jd_item_obj = JDItemDocument.objects.filter(jd_id = jd_id).first()
        if _jd_item_obj != None:
            _inst = cls(str(_jd_item_obj.id))
            _inst.item_obj = _jd_item_obj
            return _inst 
        return None

    @classmethod
    def create_jd_item(cls,entity_id, images, jd_id, cid, title, shop_nick, price, soldout, weight=0):

        _jd_id = jd_id.strip()
        _title = title.strip()
        _shop_nick = shop_nick.strip()
        _item_obj = JDItemDocument(
            entity_id = entity_id,
            images = images,
            source = 'jd',
            jd_id = _jd_id,
            cid = cid,
            title = _title,
            shop_nick = _shop_nick,
            price = price,
            soldout = soldout,
            weight = weight,
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now()
        )
        
        _item_obj.save()
        _inst = cls(_item_obj.id)
        _inst.item_obj = _item_obj
        return _inst
    
    
    def read(self):
        self.__ensure_item_obj()
        if self.item_obj.source == 'jd':
            _context = self.__load_jd_item()
        return _context
    
    def __load_jd_item(self):
        _context = {}
        _context["item_id"] = str(self.item_obj.id)
        _context["entity_id"] = self.item_obj.entity_id
        _context["source"] = self.item_obj.source
        _context["jd_id"] = self.item_obj.jd_id
        _context["cid"] = self.item_obj.cid
        _context["title"] = self.item_obj.title
        _context["shop_nick"] = self.item_obj.shop_nick
        _context["price"] = float(self.item_obj.price)
        _context["weight"] = self.item_obj.weight
        _context["soldout"] = self.item_obj.soldout
        _context['buy_link'] = get_jd_url(str(self.item_obj.jd_id))
        _context["volume"] = 0 
        return _context
    
    @classmethod
    def find(cls, entity_id = None, offset = 0, count = 30, full_info = False):
        _hdl = JDItemDocument.objects.all()
        if entity_id != None:
            _entity_id = int(entity_id)
            _hdl = _hdl.filter(entity_id = _entity_id)
        _item_list = []
        for _doc in _hdl.order_by('-weight', '-created_time')[offset : offset + count]:
            if full_info:
                _item_list.append({
                    'item_id' : str(_doc.id),
                    'jd_id' : _doc.taobao_id,
                    'entity_id' : _doc.entity_id,
                })
            else:
                _item_list.append(str(_doc.id))
        return _item_list
