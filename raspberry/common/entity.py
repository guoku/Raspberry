# coding=utf8
from models import Entity as RBEntityModel
from models import Entity_Image as RBEntityImageModel
import datetime
import urllib
from utils.lib import cal_guoku_hash 
from utils.mango_client import MangoApiClient

class RBEntity(object):
    
    def __init__(self, entity_id):
        self.__entity_id = int(entity_id)
    
    @classmethod
    def cal_entity_hash(cls, entity_hash_string):
        while True:
            entity_hash = cal_guoku_hash(entity_hash_string)
            try:
                Entity.objects.get(entity_hash = entity_hash)
            except:
                break
        return entity_hash
    
    def get_entity_id(self):
        return self.__entity_id
    
    @staticmethod
    def check_taobao_item_exist(tabao_id):
        try:
            _mango_client = MangoApiClient()
            return _mango_client.check_taobao_item(taobao_id)
        except:
            pass
        return None
    
    def add_taobao_item(self, taobao_id, **kwargs):
        _mango_client = MangoApiClient()
        _item_id = _mango_client.add_taobao_item_for_entity(self.__entity_id, taobao_id, **kwargs)
    
    
    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = RBEntityModel.objects.get(pk = self.__entity_id)

    def __ensure_entity_image_obj(self):
        if not hasattr(self, '__entity_image_obj'):
            self.__entity_image_obj = RBEntityImageModel.objects.filter(entity = self.__entity_id)[0:1].get()
    
    def __load_entity_context(self):
        self.__ensure_entity_obj()
        self.__ensure_entity_image_obj()
        _context = {}
        _context["entity_hash"] = self.__entity_obj.entity_hash
        _context["category_id"] = self.__entity_obj.category_id
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
        _context["image_url"] = self.__entity_image_obj.image_url
        return _context
        

    def read(self):
        _mango_client = MangoApiClient()
        _base_info = _mango_client.read_entity(self.__entity_id)
        _context = self.__load_entity_context()
        _context['base_info'] = _base_info
        return _context    
    
    def update(self, category_id = None, brand = None, title = None):
        if brand != None or title != None:
            _mango_client = MangoApiClient()
            _base_info = _mango_client.read_entity(self.__entity_id)
            
            if brand != None and _base_info["brand"] == brand:
                brand = None
            if title != None and _base_info["title"] == title:
                title = None
            if brand != None or title != None:
                _mango_client.update_entity(self.__entity_id, brand, title)
        
        if category_id != None:
            self.__ensure_entity_obj()
            self.__entity_obj.category_id = int(category_id)
            self.__entity_obj.save()
            
   
    @classmethod
    def read_entities(cls, entity_id_list):
        _mango_client = MangoApiClient()
        _base_datum = _mango_client.read_entities(entity_id_list)
        
        _context_list = []
        for _entity_id in entity_id_list:
            if _base_datum.has_key(str(_entity_id)):
                if _base_datum[str(_entity_id)]['status'] == '0':
                    _context = cls(_entity_id).read()
                    _context['base_info'] = _base_datum[str(_entity_id)]['context']
                    _context_list.append(_context)
        return _context_list
             
       
    @classmethod
    def find(cls, category_id = None, offset = 0, count = 30):
        _hdl = RBEntityModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        _hdl = _hdl.order_by('-created_time')[offset : offset + count]
        _entity_id_list = map(lambda x: x.id, _hdl)
        return _entity_id_list
        
    def unbind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.unbind_entity_item(self.__entity_id, item_id)
         

