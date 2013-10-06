from django.conf import settings
from ontology.entity import Entity 
from ontology.item import Item 

class MangoApiClient(object):
    
    def check_taobao_item_exist(self, taobao_id):
        return Item.get_entity_id_by_taobao_id(taobao_id)

        
    def create_entity_by_taobao_item(self, taobao_item_info, brand = "", title = "", intro = ""):
        _entity = Entity.create_by_taobao_item(
            brand = brand,
            title = title,
            intro = intro, 
            taobao_item_info = taobao_item_info 
        )
        return _entity.get_entity_id()
        

    def add_taobao_item_for_entity(self, entity_id, taobao_id, **kwargs):
        _entity = Entity(entity_id)
        _item_id = _entity.add_taobao_item(
            taobao_item_info = { 
                'taobao_id' : taobao_id, 
                'cid' : kwargs['cid'], 
                'title' : kwargs['title'], 
                'shop_nick' : kwargs['taobao_shop_nick'], 
                'price' : kwargs['taobao_price'], 
                'soldout' : kwargs['taobao_soldout'] 
            },
        )
        return _item_id
        

    def read_entity(self, entity_id):
        _entity = Entity(entity_id)
        return _entity.read()
        
    def read_item(self, item_id):
        _item = Item(item_id)
        return _item.read()
         
    def update_entity(self, entity_id, brand = None, title = None, intro = None):
        Entity(entity_id).update(
            brand = brand,
            title = title,
            intro = intro
        )
         
         
    def unbind_entity_item(self, entity_id, item_id):
        _entity = Entity(entity_id)
        _entity.del_taobao_item(item_id)
         
         
