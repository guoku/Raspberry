# coding=utf8
from models import Entity as EntityModel
from models import EntityImage as EntityImageModel
from image import Image
from item import Item
import datetime 

class Entity(object):
    
    def __init__(self, entity_id):
        self.__entity_id = entity_id
    
    def get_entity_id(self):
        return self.__entity_id
    
    def _insert_taobao_item(self, taobao_item_info, images):
        _taobao_item_obj = Item.create_taobao_item( 
            entity_id = self.__entity_id,
            images = images,
            taobao_id = taobao_item_info["taobao_id"],
            cid = taobao_item_info["cid"],
            title = taobao_item_info["title"],
            shop_nick = taobao_item_info["shop_nick"], 
            price = taobao_item_info["price"], 
            soldout = taobao_item_info["soldout"], 
        )
        return _taobao_item_obj.get_item_id()
    
    def add_taobao_item(self, taobao_item_info, image_urls):
        _image_ids = []
        for _image_url in image_urls:
            _image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], _image_url)
            _image_ids.append(_image_obj.get_image_id())
        
        _item_id = self._insert_taobao_item( 
            taobao_item_info = taobao_item_info,
            images = _image_ids
        )
        
        self.__ensure_entity_obj()
        if taobao_item_info['price'] < self.__entity_obj.price:
            self.__entity_obj.price = taobao_item_info['price']
            self.__entity_obj.updated_time = datetime.datetime.now()
            self.__entity_obj.save()
        return _item_id 

    def del_taobao_item(self, item_id):
        _item_obj = Item(item_id)
        if _item_obj.get_entity_id() == self.__entity_id:
            _item_obj.bind_entity("")
    
    @classmethod
    def create_by_taobao_item(cls, brand, title, intro, taobao_item_info, chief_image_url, detail_image_urls):
        
        if brand != None: 
            brand = brand.strip()
        if title != None:
            title = title.strip()
        if intro != None:
            intro = intro.strip()
        
        _chief_image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], chief_image_url)
        _chief_image_id = _chief_image_obj.get_image_id()
        _detail_image_ids = []
        for _image_url in detail_image_urls:
            _image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], _image_url)
            _detail_image_ids.append(_image_obj.get_image_id())
        
        _price = taobao_item_info['price']
        _entity_obj = EntityModel(
            brand = brand,
            title = title,
            intro = intro,
            price = _price,
            images = EntityImageModel(
                chief_id = _chief_image_id,
                detail_ids = _detail_image_ids
            ),
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        _entity_obj.save()
        
        _inst = cls(str(_entity_obj.id))
        _inst.__entity_obj = _entity_obj
        
        try:
            _item_images = _detail_image_ids
            _item_images.append(_chief_image_id)
            _taobao_item_id = _inst._insert_taobao_item(taobao_item_info, _item_images)
        except Exception, e:
            _entity_obj.delete()
            raise e

        return _inst

    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = EntityModel.objects.get(pk = self.__entity_id) 
    
    def read(self):
        self.__ensure_entity_obj()
        _context = {}
        _context['entity_id'] = str(self.__entity_obj.id)
        _context['brand'] = self.__entity_obj.brand 
        _context['title'] = self.__entity_obj.title
        _context['intro'] = self.__entity_obj.intro
        if self.__entity_obj.price:
            _context['price'] = float(self.__entity_obj.price)
        else:
            _context['price'] = 0.0 
        _context['chief_image'] = { 'url' : Image(self.__entity_obj.images.chief_id).getlink() }
        _context['detail_images'] = []
        for _image_id in self.__entity_obj.images.detail_ids:
            _context['detail_images'].append({
                'url' : Image(_image_id).getlink()
            })
        _context['item_id_list'] = Item.get_item_id_list_by_entity_id(self.__entity_id) 
        return _context    
    
    def update(self, brand = None, title = None, intro = None, price = None):
        self.__ensure_entity_obj()
        if brand != None:
            self.__entity_obj.brand = brand
        if title != None:
            self.__entity_obj.title = title
        if intro != None:
            self.__entity_obj.intro = intro
        if price != None:
            self.__entity_obj.price = price
        self.__entity_obj.updated_time = datetime.datetime.now()
        self.__entity_obj.save()
