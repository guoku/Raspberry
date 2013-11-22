import datetime
import MySQLdb
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

    meta = {
        'indexes' : [ 
            'taobao_id',
            'cid',
            'shop_nick',
            'price',
            'soldout'
        ],
    }
    

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")

print 'adding base_neo_category & base_neo_category_group...'
cur_gk.execute('CREATE TABLE base_neo_category_group AS (SELECT * FROM raspberry.common_neo_category_group);')
cur_gk.execute('ALTER TABLE base_neo_category_group ENGINE=InnoDB;')
cur_gk.execute('ALTER TABLE base_neo_category_group CHANGE id id INT(11) AUTO_INCREMENT PRIMARY KEY;')
cur_gk.execute('ALTER TABLE base_neo_category_group ADD KEY `common_category_group_title` (`title`);')
cur_gk.execute('ALTER TABLE base_neo_category_group ADD KEY `common_category_group_status` (`status`);')

cur_gk.execute('CREATE TABLE base_neo_category AS (SELECT * FROM raspberry.common_neo_category);')
cur_gk.execute('ALTER TABLE base_neo_category ENGINE=InnoDB;')
cur_gk.execute('ALTER TABLE base_neo_category CHANGE id id INT(11) AUTO_INCREMENT PRIMARY KEY;')
cur_gk.execute('ALTER TABLE base_neo_category ADD KEY `common_category_group_id` (`group_id`);')
cur_gk.execute('ALTER TABLE base_neo_category ADD KEY `common_category_title` (`title`);')
cur_gk.execute('ALTER TABLE base_neo_category ADD KEY `common_category_status` (`status`);')
cur_gk.execute('ALTER TABLE base_neo_category ADD KEY `common_category_image_store_hash` (`image_store_hash`);')
cur_gk.execute('ALTER TABLE base_neo_category ADD CONSTRAINT `group_id_refs_id_ce893429` FOREIGN KEY (`group_id`) REFERENCES `base_neo_category_group` (`id`);')

print 'updating base_entity...'
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `neo_category_id` int(11) NOT NULL;')
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `intro` longtext NOT NULL;')
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `price` decimal(20,2) NOT NULL;')
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `like_count` int(11) NOT NULL DEFAULT 0;')
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `chief_image` varchar(64) NOT NULL;')
cur_gk.execute('ALTER TABLE base_entity ADD COLUMN `detail_images` varchar(1024) NOT NULL;')
cur_gk.execute('ALTER TABLE base_entity ADD KEY `common_entity_neo_category_id` (`neo_category_id`);')
cur_gk.execute('ALTER TABLE base_entity ADD KEY `common_entity_price` (`price`);')
cur_gk.execute('ALTER TABLE base_entity ADD KEY `common_entity_like_count` (`like_count`);')
cur_gk.execute('ALTER TABLE base_entity CHANGE creator_id `creator_id` int(11);')
cur_gk.execute("UPDATE base_entity INNER JOIN ( SELECT entity_id, COUNT(*) AS tot FROM guoku_entity_like GROUP BY entity_id ) AS elt ON base_entity.id=elt.entity_id SET base_entity.like_count=elt.tot;")

print 'updating base_note...'
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `entity_id` int(11) NOT NULL;')
cur_gk.execute('UPDATE base_note LEFT JOIN base_entity_note ON base_note.id=base_entity_note.note_id SET base_note.entity_id=base_entity_note.entity_id;')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_note_entity_id` (`entity_id`);')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `score` int(11) NOT NULL DEFAULT 0;')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_note_score` (`score`);')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `figure` varchar(256) NOT NULL;')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `post_time` datetime DEFAULT NULL;')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `selector_id` int(11) DEFAULT NULL;')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `selected_time` datetime DEFAULT NULL;')
cur_gk.execute('ALTER TABLE base_note ADD COLUMN `weight` int(11) NOT NULL DEFAULT 0;')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_entity_note_post_time` (`post_time`);')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_entity_note_selector_id` (`selector_id`);')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_entity_note_selected_time` (`selected_time`);')
cur_gk.execute('ALTER TABLE base_note ADD KEY `base_entity_note_weight` (`weight`);')
cur_gk.execute('UPDATE base_note INNER JOIN base_entity_note ON base_note.id=base_entity_note.note_id SET base_note.post_time=base_entity_note.post_time, base_note.selector_id=base_entity_note.selector_id, base_note.selected_time=base_entity_note.selected_time, base_note.weight=base_entity_note.weight;')


fi = open('cats_matching.txt', 'r')
tb_cat_match = {}
for line in fi.readlines():
    line = line.strip()
    tokens = line.split('\t') 
    tb_cat_match[int(tokens[0])] = int(tokens[1])

cur_gk.execute("select base_entity.id, base_item.id from base_entity inner join base_item on base_entity.id=base_item.entity_id")
entity_dict = {}
for row in cur_gk.fetchall():
    entity_id = row[0]
    item_id = row[1]
    if not entity_dict.has_key(entity_id):
        entity_dict[entity_id] = []
    entity_dict[entity_id].append(item_id)

connect('guoku', host = 'localhost') 
Item.drop_collection()
Image.drop_collection()
count = 0
for entity_id in entity_dict.keys():
    neo_category_id = 0
    price = 0.0 
    for item_id in entity_dict[entity_id]:
        cur_gk.execute("select taobao_id, taobao_category_id, title, shop_nick, price, soldout, created_time, updated_time FROM base_taobao_item WHERE item_id=%d"%item_id)
        row = cur_gk.fetchone()
        if row != None: 
            shop_nick = row[3]
            if shop_nick == None:
                shop_nick = ''
            if row[1] != None:
                if row[5] == 1:
                    soldout = True
                else:
                    soldout = False
                item_obj = TaobaoItem( 
                    entity_id = entity_id,
                    images = [],
                    source = 'taobao',
                    taobao_id = row[0],
                    cid = row[1],
                    title = row[2],
                    shop_nick = shop_nick,
                    price = row[4],
                    soldout = soldout, 
                    created_time = row[6], 
                    updated_time = row[7] 
                )
                item_obj.save() 
                if neo_category_id == 0 and tb_cat_match.has_key(row[1]):
                    neo_category_id = tb_cat_match[row[1]]
                if price == 0.0 or row[4] < price:
                    price = row[4]
            else:
                print "entity[%d] item[%d] has no category..."%(entity_id, item_id)
        else:
            print "entity[%d] item[%d] can't be found in item..."%(entity_id, item_id)
    cur_gk.execute("select image_url FROM base_entity_image WHERE entity_id=%d"%entity_id)
    row = cur_gk.fetchone()
    if row != None:
        origin_url = row[0].replace('_310x310.jpg', '')

        image_obj = Image.objects.filter(origin_url = origin_url).first()
        if image_obj == None:
            image_obj = Image( 
                source = 'gk_old', 
                origin_url = origin_url, 
                created_time = datetime.datetime.now(),
                updated_time = datetime.datetime.now() 
            )
            image_obj.save()
        cur_gk.execute("UPDATE base_entity SET neo_category_id=%d, chief_image='%s', price=%f  WHERE id=%d"%(neo_category_id, str(image_obj.id), price, entity_id))
    count += 1
    if count % 1000 == 0:
        print "%d entities processed..."%count
    
cur_gk.execute('update base_entity set neo_category_id=300 where neo_category_id=0;')
cur_gk.execute('ALTER TABLE base_entity DROP INDEX entity_hash;')
cur_gk.execute("INSERT INTO base_entity (id, brand, title, category_id, creator_id, created_time, updated_time, weight, entity_hash, neo_category_id, intro, price, chief_image, detail_images) SELECT id, brand, title, 12, creator_id, created_time, updated_time, weight, CONCAT(entity_hash, 'rb'), neo_category_id, intro, price, chief_image, detail_images FROM raspberry.common_entity;")
conn_gk.commit()



########## TRANSPORT MANGO IMAGE DATA ########
########## TRANSPORT MANGO ITEM DATA ########
########## INITIAL SELECTION DATA ########
########## REMOVE MARIA IN AVOCADO SETTING ########
########## REMOVE MARIA_WEB IN AVOCADO SETTING ########

