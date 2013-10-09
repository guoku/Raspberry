# coding=utf8
from models import Entity as RBEntityModel
from hashlib import md5
import datetime
import urllib
from utils.lib import cal_guoku_hash 
from mango.client import MangoApiClient

class RBEntity(object):
    
    def __init__(self, entity_id):
        self.__entity_id = entity_id
    
    @classmethod
    def cal_entity_hash(cls, entity_hash_string):
        while True:
            _hash = md5(entity_hash_string + unicode(datetime.datetime.now())).hexdigest()[0:8]
            try:
                Entity.objects.get(entity_hash = _hash)
            except:
                break
        return _hash 
    
    def get_entity_id(self):
        return self.__entity_id
    
    @staticmethod
    def check_taobao_item_exist(taobao_id):
        _mango_client = MangoApiClient()
        return _mango_client.check_taobao_item_exist(taobao_id)
    
    @classmethod
    def create_by_taobao_item(cls, creator_id, category_id, chief_image_url, 
                              taobao_item_info, brand = "", title = "", intro = "", detail_image_urls = []):
        
        _mango_client = MangoApiClient()
        _entity_id = _mango_client.create_entity_by_taobao_item(
            taobao_item_info = taobao_item_info,
            chief_image_url = chief_image_url,
            brand = brand,
            title = title,
            intro = intro,
            detail_image_urls = detail_image_urls
        )
       
        _entity_hash = cls.cal_entity_hash(taobao_item_info['taobao_id'])
        _entity_obj = RBEntityModel.objects.create( 
            entity_id = _entity_id,
            entity_hash = _entity_hash,
            category_id = category_id,
            creator_id = creator_id
        )
         
        _inst = cls(_entity_obj.entity_id)
        _inst.__entity_obj = _entity_obj
        return _inst

    
    def add_taobao_item(self, taobao_item_info):
        _mango_client = MangoApiClient()
        _item_id = _mango_client.add_taobao_item_for_entity(self.__entity_id, taobao_item_info)
    
    
    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = RBEntityModel.objects.get(entity_id = self.__entity_id)

    def __load_entity_context(self):
        self.__ensure_entity_obj()
        _context = {}
        _context["entity_hash"] = self.__entity_obj.entity_hash
        _context["category_id"] = self.__entity_obj.category_id
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
        return _context
        

    def read(self):
        _mango_client = MangoApiClient()
        _meta_info = _mango_client.read_entity(self.__entity_id)
        _context = self.__load_entity_context()
        _context['meta'] = _meta_info
        return _context    
    
    def update(self, category_id = None, brand = None, title = None, intro = None):
        if brand != None or title != None or intro != None:
            _mango_client = MangoApiClient()
            _base_info = _mango_client.read_entity(self.__entity_id)
            
            if _base_info["brand"] == brand:
                brand = None
            if _base_info["title"] == title:
                title = None
            if _base_info["intro"] == intro:
                intro = None
            if brand != None or title != None or intro != None:
                _mango_client.update_entity(
                    entity_id = self.__entity_id, 
                    brand = brand, 
                    title = title, 
                    intro = intro
                )
        
        if category_id != None:
            self.__ensure_entity_obj()
            self.__entity_obj.category_id = int(category_id)
            self.__entity_obj.save()
            
   
    @classmethod
    def read_entities(cls, entity_id_list):
        _mango_client = MangoApiClient()
        _context_list = []
        for _entity_id in entity_id_list:
            _context = cls(_entity_id).read()
            _context['base_info'] = _mango_client.read_entity(_entity_id)
            _context_list.append(_context)
        return _context_list
             
       
    @classmethod
    def find(cls, category_id = None, offset = 0, count = 30):
        _hdl = RBEntityModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        _hdl = _hdl.order_by('-created_time')[offset : offset + count]
        _entity_id_list = map(lambda x: x.entity_id, _hdl)
        return _entity_id_list
        
    @classmethod
    def count(cls, category_id = None):
        _hdl = RBEntityModel.objects.filter(category_id = category_id)
        return _hdl.count()
    
    def unbind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.unbind_entity_item(self.__entity_id, item_id)
         

