import pymongo
import datetime
import MySQLdb
from bson.objectid import ObjectId


client = pymongo.Connection('localhost', 27017)
db = client['mango']
entity_coll = db['entity']
item_coll = db['item']

conn = MySQLdb.Connection("localhost", "root", "123456", "raspberry_11_08")
cur = conn.cursor()
cur.execute("SET names utf8")

cur.execute('ALTER TABLE common_entity ADD COLUMN `brand` varchar(256) DEFAULT NULL;')
cur.execute('ALTER TABLE common_entity ADD COLUMN `title` varchar(256) DEFAULT NULL;')
cur.execute('ALTER TABLE common_entity ADD COLUMN `price` decimal(20,2) NOT NULL;')
cur.execute('ALTER TABLE common_entity ADD KEY `common_entity_price` (`price`);')
cur.execute('ALTER TABLE common_entity ADD COLUMN `intro` longtext;')
cur.execute('ALTER TABLE common_entity ADD COLUMN `chief_image` varchar(64) NOT NULL;')
cur.execute('ALTER TABLE common_entity ADD COLUMN `detail_images` varchar(1024) DEFAULT NULL;')
cur.execute('ALTER TABLE common_entity ADD COLUMN `is_candidate` tinyint(1) NOT NULL;')
cur.execute('ALTER TABLE common_entity ADD KEY `common_entity_e4b99077` (`is_candidate`);')


mango_entities = [] 
for entity in entity_coll.find():
    row = {
        '_id' : entity['_id'],
        'brand' : conn.escape_string(entity['brand'].encode('utf-8')),
        'title' : conn.escape_string(entity['title'].encode('utf-8')),
        'intro' : conn.escape_string(entity['intro'].encode('utf-8')),
        'chief_image' : entity['images']['chief_id'].encode('utf-8'),
        'detail_images' : entity['images']['detail_ids'],
    }
    if entity.has_key('price'):
        row['price'] = entity['price']
    else:
        row['price'] = 0.0 
        print "entity [%s] price miss..."%entity['_id']
    mango_entities.append(row)


delta = 200003
for entity in mango_entities:
    cur.execute("select id from common_entity where entity_id='%s';"%entity['_id'])
    row = cur.fetchone()
    if row != None:
        entity_id = row[0]
        entity_id_new = entity_id + delta
        detail_images_str = '#'.join(entity['detail_images']).encode('utf-8')
        cur.execute("update common_entity set id=%d, brand='%s', title='%s', intro='%s', price=%f, chief_image='%s', detail_images='%s' where id=%d;"%(entity_id_new, entity['brand'], entity['title'], entity['intro'], entity['price'], entity['chief_image'], detail_images_str, entity_id))
        entity_coll.update({ "_id" : ObjectId(entity['_id']) }, { "$set" : { "entity_id" : entity_id_new }})
        
conn.commit()

cur.execute('DROP TABLE common_note_poke;')
cur.execute('DROP TABLE common_note_figure;')
cur.execute('DROP TABLE common_note_comment;')
cur.execute('DROP TABLE common_entity_note;')
cur.execute('DROP TABLE common_candidate_note;')
cur.execute('DROP TABLE common_candidate_ask;')
cur.execute('DROP TABLE common_candidate;')
cur.execute('DROP TABLE common_note;')
cur.execute('DROP TABLE common_entity_like;')
