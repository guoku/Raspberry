# coding=utf8
from mongoengine import *

class EntityImage(EmbeddedDocument):
    chief_id = StringField(required = True)
    detail_ids = ListField(required = False)
    

class Entity(Document):
    brand = StringField(required = True)
    title = StringField(required = True)
    intro = StringField(required = False)
    images = EmbeddedDocumentField('EntityImage', required = True)
    price = DecimalField(required = True)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'db_alias' : 'mango',
        'indexes' : [ 
            'brand',
            'title',
            'price',
        ],
        'allow_inheritance' : True
    }

class Image(Document):
    source = StringField(required = True)
    origin_url  = URLField(required = False, unique = True)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'db_alias' : 'mango',
        'indexes' : [ 
            'source' 
        ],
        'allow_inheritance' : True
    }

class Item(Document):
    entity_id = StringField(required = True) 
    source = StringField(required = True)
    images = ListField(required = False)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'db_alias' : 'mango',
        'indexes' : [ 
            'entity_id' 
        ],
        'allow_inheritance' : True
    }

class TaobaoItem(Item):
    taobao_id = StringField(required = True, unique = True)
    cid = IntField(required = True) 
    title = StringField(required = True)
    shop_nick = StringField(required = True)
    price = DecimalField(required = True)
    soldout = BooleanField(required = True) 

    meta = {
        'db_alias' : 'mango',
        'indexes' : [ 
            'taobao_id',
            'cid',
            'shop_nick',
            'price',
            'soldout'
        ],
    }
    
