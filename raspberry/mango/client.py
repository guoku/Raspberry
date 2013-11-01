from django.conf import settings
from ontology.entity import Entity 
from ontology.item import Item 

class MangoApiClient(object):
    
    def check_taobao_item_exist(self, taobao_id):
        return Item.get_entity_id_by_taobao_id(taobao_id)

    def get_item_id_by_taobao_id(self, taobao_id):
        return Item.get_item_id_by_taobao_id(taobao_id)
        
    def create_entity_by_taobao_item(self, taobao_item_info, chief_image_url, brand = "", title = "", intro = "", detail_image_urls = []):
        _entity = Entity.create_by_taobao_item(
            brand = brand,
            title = title,
            intro = intro, 
            taobao_item_info = taobao_item_info,
            chief_image_url = chief_image_url,
            detail_image_urls = detail_image_urls
        )
        return _entity.get_entity_id()
        

    def add_taobao_item_for_entity(self, entity_id, taobao_item_info, image_urls):
        _item_id = Entity(entity_id).add_taobao_item(
            taobao_item_info = taobao_item_info,
            image_urls = image_urls
        )
        return _item_id
        

    def read_entity(self, entity_id):
        _entity = Entity(entity_id)
        return _entity.read()
        
    def read_item(self, item_id):
        _item = Item(item_id)
        return _item.read()
         
    def update_entity(self, entity_id, brand = None, title = None, intro = None, price = None, chief_image_id = None):
        _entity = Entity(entity_id)
        _entity.update(
            brand = brand,
            title = title,
            intro = intro,
            price = price,
            chief_image_id = chief_image_id
        )
    
    def sort_entity_by_price(self, entity_id_list, reverse = False):
        return Entity.sort_by_price(entity_id_list, reverse)
         
         
    def bind_entity_item(self, entity_id, item_id):
        _entity = Entity(entity_id)
        _entity.bind_taobao_item(item_id)
         
    def unbind_entity_item(self, entity_id, item_id):
        _entity = Entity(entity_id)
        _entity.unbind_taobao_item(item_id)
         
    def search_entity(self, query):
        return Entity.search(query)
         
    def find_item(self, offset = 0, count = 30):
        return Item.find(offset, count)
