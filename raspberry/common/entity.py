# coding=utf8
from models import Entity as RBEntityModel
import datetime 
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
    
    @classmethod
    def create_by_taobao_item(cls, creator_id, taobao_id, **kwargs):
        _mango_client = MangoApiClient()
        _entity_id = _mango_client.create_entity_by_taobao_item(taobao_id, **kwargs)
        _entity_hash = cls.cal_entity_hash(taobao_id)
        _entity_obj = RBEntityModel.objects.create( 
            id = _entity_id,
            entity_hash = _entity_hash,
            creator_id = creator_id
        )
        

        _inst = cls(_entity_obj.id)
        _inst.__entity_obj = _entity_obj
        return _inst

    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = Entity.objects.get(pk = self.__entity_id) 
    
    def read(self):
        _context = {}
        
        _context["entity_id"] = self.__entity_obj.id
        _context["entity_hash"] = self.__entity_obj.entity_hash
        _context["brand"] = self.__entity_obj.brand 
        _context["title"] = self.__entity_obj.title
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
            
        return _context    
