import pymongo
import datetime
import MySQLdb
from bson.objectid import ObjectId


conn = MySQLdb.Connection("localhost", "root", "123456", "guoku_11_06_slim")
cur = conn.cursor()
cur.execute("SET names utf8")

cur.execute('CREATE TABLE base_neo_category_group AS (SELECT * FROM raspberry_11_12.common_neo_category_group);')
cur.execute('CREATE TABLE base_neo_category AS (SELECT * FROM raspberry_11_12.common_neo_category);')
cur.execute('ALTER TABLE base_note ADD COLUMN `entity_id` int(11) NOT NULL;')
cur.execute('UPDATE base_note LEFT JOIN base_entity_note ON base_note.id=base_entity_note.note_id SET base_note.entity_id=base_entity_note.entity_id;')
cur.execute('ALTER TABLE base_note ADD KEY `base_note_entity_id` (`entity_id`);')
cur.execute('ALTER TABLE base_note ADD COLUMN `score` int(11) NOT NULL;')
cur.execute('ALTER TABLE base_note ADD KEY `base_note_score` (`score`);')
cur.execute('ALTER TABLE base_note ADD COLUMN `figure` varchar(256) NOT NULL;')
#cur.execute('DELETE base_note_comment.* from base_note_comment INNER JOIN base_note ON base_note_comment.note_id=base_note.id WHERE base_note.entity_id=0;')
#cur.execute('DELETE base_note_poke.* from base_note_poke INNER JOIN base_note ON base_note_poke.note_id=base_note.id WHERE base_note.entity_id=0;')
#cur.execute('DELETE base_note_hoot.* from base_note_hoot INNER JOIN base_note ON base_note_hoot.note_id=base_note.id WHERE base_note.entity_id=0;')


#mango_entities = [] 
#for entity in entity_coll.find():
#    row = {
#        '_id' : entity['_id'],
#        'brand' : conn.escape_string(entity['brand'].encode('utf-8')),
#        'title' : conn.escape_string(entity['title'].encode('utf-8')),
#        'intro' : conn.escape_string(entity['intro'].encode('utf-8')),
#        'chief_image' : entity['images']['chief_id'].encode('utf-8'),
#    }
#    
#    if entity['images'].has_key('detail_ids'):
#        row['detail_images'] = entity['images']['detail_ids']
#    else:
#        row['detail_images'] = []
#    
#    if entity.has_key('price'):
#        row['price'] = entity['price']
#    else:
#        row['price'] = 0.0 
#    mango_entities.append(row)
#
#
#delta = 200003
#count = 0
#for entity in mango_entities:
#    cur.execute("select id from common_entity where entity_id='%s';"%entity['_id'])
#    row = cur.fetchone()
#    if row != None:
#        entity_id = row[0]
#        entity_id_new = entity_id + delta
#        detail_images_str = '#'.join(entity['detail_images']).encode('utf-8')
#        cur.execute("update common_entity set id=%d, brand='%s', title='%s', intro='%s', price=%f, chief_image='%s', detail_images='%s' where id=%d;"%(entity_id_new, entity['brand'], entity['title'], entity['intro'], entity['price'], entity['chief_image'], detail_images_str, entity_id))
#        entity_coll.update({ "_id" : ObjectId(entity['_id']) }, { "$set" : { "entity_id" : entity_id_new }})
#        item_id_list = []
#        for item in item_coll.find({ "entity_id" : str(entity['_id'])}):
#            item_id_list.append(item['_id'])
#        for item_id in item_id_list:
#            item_coll.update({ "_id" : ObjectId(item_id) }, { "$set" : { "entity_id" : entity_id_new }})
#    count += 1
#    if count % 1000 == 0:
#        print "%d entities processed..."%count
#
#cur.execute('DROP TABLE common_note_poke;')
#cur.execute('DROP TABLE common_note_figure;')
#cur.execute('DROP TABLE common_note_comment;')
#cur.execute('DROP TABLE common_entity_note;')
#cur.execute('DROP TABLE common_candidate_note;')
#cur.execute('DROP TABLE common_candidate_ask;')
#cur.execute('DROP TABLE common_candidate;')
#cur.execute('DROP TABLE common_note;')
#cur.execute('DROP TABLE common_entity_like;')
#cur.execute('ALTER TABLE common_entity DROP COLUMN entity_id;')
#conn.commit()
