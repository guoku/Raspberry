import datetime
import MySQLdb
from mongoengine import * 

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

    meta = {
        'indexes' : [ 
            'taobao_id',
            'cid',
            'shop_nick',
            'price',
            'soldout'
        ],
    }
    

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_11_21")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")


cur_gk.execute("select taobao_category_id, guoku_category_id from base_taobao_item_category_mapping;")
category_dict = {}
for row in cur_gk.fetchall():
    cid = row[0]
    guoku_category_id = row[1]
    category_dict[cid] = guoku_category_id

cur_gk.execute("select id from base_entity where category_id=12;")
entity_list = [] 
for row in cur_gk.fetchall():
    entity_list.append(row[0])


connect('guoku', host = 'localhost')
changed_count = 0
it_count = 0
for entity_id in entity_list:
    it_count += 1
    item_obj = TaobaoItem.objects.filter(entity_id = entity_id).first()
    if item_obj != None:
        if category_dict.has_key(item_obj.cid):
            guoku_category_id = category_dict[item_obj.cid]
            if guoku_category_id != 12:
                sql_query = "update base_entity set category_id=%d where id=%d;"%(guoku_category_id, entity_id)
                cur_gk.execute("update base_entity set category_id=%d where id=%d;"%(guoku_category_id, entity_id))
                changed_count += 1
    if it_count % 1000 == 0:
        print "%d / %d / %d ..."%(changed_count, it_count, len(entity_list))
conn_gk.commit()
