import sys
sys.path.append("..")
from mango.ontology.models import Entity, EntityImage, Image, Item, TaobaoItem 
from mongoengine import connect
import datetime
import MySQLdb


conn_mango = MySQLdb.Connection("localhost", "root", "123456", "mango")
cur_mango = conn_mango.cursor()
cur_mango.execute("SET names utf8")
conn_raspberry = MySQLdb.Connection("localhost", "root", "123456", "raspberry")
cur_raspberry = conn_raspberry.cursor()
cur_raspberry.execute("SET names utf8")


connect('mango', 'localhost') 
Entity.drop_collection()
Image.drop_collection()

import pymongo
client = pymongo.Connection('localhost', 27017)
db = client['mango']
item_coll = db['item_old']

cur_mango.execute("select * from ontology_entity;")
for row in cur_mango.fetchall():
    _id = row[0]
    _brand = row[1]
    _title = row[2]
    _intro = row[3]
    _created_time = row[4]
    _updated_time = row[5]
    
    cur_raspberry.execute("select * from common_entity_image where entity_id=%d;"%_id)
    _row = cur_raspberry.fetchone()
    _image_url = _row[2]
    
    _image_obj = Image( 
        source = 'tb_unknown',
        origin_url = _image_url,
        created_time = datetime.datetime.now(),
        updated_time = datetime.datetime.now() 
    )
    _image_obj.save()
    
    _entity_obj = Entity(
        brand = unicode(_brand.decode('utf8')),
        title = unicode(_title.decode('utf8')),
        intro = unicode(_intro.decode('utf8')),
        images = EntityImage(
            chief_id = str(_image_obj.id),
            detail_ids = [] 
        ),
        created_time = datetime.datetime.now(),
        updated_time = datetime.datetime.now() 
    )
    _entity_obj.save()

    for _item in item_coll.find({ "entity_id" : _id }):
        _taobao_id = _item['taobao_id']
        _item_obj = TaobaoItem( 
            entity_id = str(_entity_obj.id),
            images = [str(_image_obj.id)],
            source = 'taobao',
            taobao_id = _item['taobao_id'],
            cid = _item['cid'],
            title = _item['title'],
            shop_nick = _item['shop_nick'],
            price = _item['price'],
            soldout = _item['soldout'],
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        _item_obj.save()
   
    cur_raspberry.execute("select id, entity_hash, creator_id, category_id, created_time, updated_time from common_entity_old where id=%d;"%_id)
    _row = cur_raspberry.fetchone()
    _id = _row[0]
    _entity_hash = _row[1]
    _creator_id = _row[2]
    _category_id = _row[3]
    _created_time = _row[4]
    _updated_time = _row[5]
    
    sql_query = "INSERT INTO common_entity (id, entity_id, entity_hash, creator_id, category_id, created_time, updated_time) VALUES "
    sql_query += "(%d, '%s', '%s', %d, %d, '%s', '%s');"%(_id, str(_entity_obj.id), _entity_hash, _creator_id, _category_id, _created_time.strftime("%Y-%m-%d %H:%M:%S"), _updated_time.strftime("%Y-%m-%d %H:%M:%S")) 

    cur_raspberry.execute(sql_query)
    
conn_mango.commit()
conn_raspberry.commit()
