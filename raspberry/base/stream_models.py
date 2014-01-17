from mongoengine import * 
class Image(Document):
    source = StringField(required = True)
    origin_url  = URLField(required = False)
    store_hash = StringField(required = False)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'indexes' : [ 
            'source',
            'origin_url',
            'store_hash',
        ],
        'allow_inheritance' : True
    }

class Item(Document):
    entity_id = IntField(required = True) 
    source = StringField(required = True)
    images = ListField(required = False)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
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
    ustation = IntField(required = False) 

    meta = {
        'indexes' : [ 
            'taobao_id',
            'cid',
            'shop_nick',
            'price',
            'soldout',
            'ustation',
        ],
    }
    
class Selection(Document):
    selector_id = IntField(required = True) 
    selected_time = DateTimeField(required = True)
    post_time = DateTimeField(required = True)
    meta = {
        "indexes" : [ 
            "selector_id", 
            "post_time" 
        ],
        "allow_inheritance" : True
    }

class NoteSelection(Selection):
    entity_id = IntField(required = True) 
    note_id = IntField(required = True) 
    root_category_id = IntField(required = True) 
    neo_category_group_id = IntField(required = True) 
    neo_category_id = IntField(required = True) 
    category_id = IntField(required = True) 
    meta = {
        "indexes" : [ 
            "entity_id", 
            "note_id",
            "root_category_id",
            "neo_category_group_id",
            "neo_category_id",
            "category_id" 
        ]
    }

class Log(Document):
    entry = StringField(required = True)
    user_id = IntField(required = True) 
    ip = StringField(required = True)
    log_time = DateTimeField(required = True)
    appendix = DictField(required = False)
    meta = {
        'db_alias' : 'log-db',
        'indexes' : [ 
            'entry',
            'user_id',
            'log_time' 
        ],
        'allow_inheritance' : True
    }

class ShopScore(EmbeddedDocument):
    credit = StringField()
    praise_rate = FloatField()

class TaobaoShopInfo(EmbeddedDocument):
    cid = IntField()
    nick = StringField(required = True, unique = True)
    pic_path = StringField()
    sid = IntField(required = True, unique = True)
    title = StringField(required = True)
    seller_id = IntField()
    company = StringField()
    shop_type = StringField()
    shop_link = StringField()
    shop_score = EmbeddedDocumentField(ShopScore)
    main_products = StringField()
    location = StringField()
    updated_time = DateTimeField()
    meta = {
        'indexes' : ['cid', 'nick', 'sid', 'seller_id','shop_type']
    }

class TaobaoShopExtendedInfo(EmbeddedDocument):
    orientational = BooleanField()
    commission_rate = FloatField()
    commission = BooleanField()
    single_tail = BooleanField()
    gifts = ListField(StringField())

class CrawlerInfo(EmbeddedDocument):
    priority = IntField(required = True)
    cycle = IntField(required = True)

class TaobaoShop(DynamicDocument):
    shop_info = EmbeddedDocumentField(TaobaoShopInfo)
    created_time = DateTimeField()
    last_updated_time = DateTimeField()
    last_crawled_time = DateTimeField()
    crawler_info = EmbeddedDocumentField(CrawlerInfo)
    extended_info = EmbeddedDocumentField(TaobaoShopExtendedInfo)
    meta = { 
        'collection' : 'taobao_shops_depot',
        'indexes' : [ 'last_updated_time' ]}
