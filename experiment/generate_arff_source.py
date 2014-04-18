import MySQLdb
import pymongo
import datetime



def load_price_distribute():
    fi = open("factor/price.fct", "r")
    price_distribute = []
    for line in fi.readlines(): 
        price_distribute.append(float(line.strip()))
    fi.close()
    return price_distribute 

def load_category_distribute():
    fi = open("factor/category.fct", "r")
    category_distribute = {} 
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        category_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()
    return category_distribute 

def load_neo_category_group_distribute():
    fi = open("factor/neo_category_group.fct", "r")
    neo_category_group_distribute = {} 
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        neo_category_group_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()
    return neo_category_group_distribute 

def load_category_parent_distribute():
    fi = open("factor/category_parent.fct", "r")
    category_parent_distribute = {} 
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        category_parent_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()
    return category_parent_distribute 

def load_entity_info():
    conn = MySQLdb.Connection("localhost", "root", "123456", "guoku")
    cur = conn.cursor()
    cur.execute("SET names utf8")
    sql_query = "select base_entity.id, base_note.post_time, price, base_entity.category_id, base_category.pid, base_entity.neo_category_id, base_neo_category.group_id from base_entity inner join base_note on base_entity.id=base_note.entity_id inner join base_category on base_entity.category_id=base_category.id inner join base_neo_category on base_entity.neo_category_id=base_neo_category.id where base_note.post_time is not null;"
    cur.execute(sql_query)
    count = 0
    entity_dict = {}
    for row in cur.fetchall():
        entity_dict[row[0]] = {
            'post_time': row[1],
            'price': row[2],
            'category_id': row[3],
            'category_parent_id': row[4],
            'neo_category_id': row[5],
            'neo_category_group_id': row[6],
            'click_count': 0
        }
        count += 1
        if count % 100000 == 0:
            print "%d entities loaded..."%count
    conn.commit()
    conn.close()
    return entity_dict

def set_price_value(price, price_distribute):
    if price == 0.0:
        value = 0.0
    else:
        value = 1.0
        for floor in price_distribute:
            if price > floor:
                break
            value -= 0.1
    return value



price_distribute = load_price_distribute()
category_distribute = load_category_distribute()
category_parent_distribute = load_category_parent_distribute()
neo_category_group_distribute = load_neo_category_group_distribute()
entity_dict = load_entity_info()

fo = open('guoku_click_log_linear_category.arff', 'w')
fo.write('@relation guoku_click_log_linear_category\n\n') 

fo.write('@attribute price NUMERIC\n')
fo.write('@attribute price_level NUMERIC\n')
fo.write('@attribute category NUMERIC\n')
fo.write('@attribute category_parent NUMERIC\n')
fo.write('@attribute neo_category_grouop NUMERIC\n')
fo.write('@attribute click NUMERIC\n\n\n')

fo.write('@data\n')
conn = pymongo.Connection('localhost', 27017)
db = conn.experiment
i = 0

#for doc in db.log_2013.find({"logged_time": {"$gt": datetime.datetime(2013, 9, 1), "$lt": datetime.datetime(2013, 10, 1)}}):
#for doc in db.log_2013.find({"logged_time": {"$lt": datetime.datetime(2013, 8, 1)}}):
for doc in db.log_2013.find():
#for doc in db.log_2013.find({"logged_time": {"$lt": datetime.datetime(2013, 4, 1)}}):
    try:
        entity_id =  doc['entity_id']
        if entity_dict.has_key(entity_id):
            if entity_dict[entity_id]['post_time'] != None:
                if entity_dict[entity_id]['post_time'] < doc['logged_time']:
                    if doc['logged_time'] - entity_dict[entity_id]['post_time'] < datetime.timedelta(hours=120):
                        entity_dict[entity_id]['click_count'] += 1
    except Exception, e:
        print e
    i += 1
    if i % 100000 == 0:
        print "%d logs processed..."%i


for entity_id, values in entity_dict.items():
    if values['click_count'] > 0:
        fo.write(str(values['price']))
        fo.write(',' + str(set_price_value(values['price'], price_distribute)))
        if category_distribute.has_key(values['category_id']):
            fo.write(',' + str(category_distribute[values['category_id']]))
        else:
            fo.write(',0.0') 
        if category_parent_distribute.has_key(values['category_parent_id']):
            fo.write(',' + str(category_parent_distribute[values['category_parent_id']]))
        else:
            fo.write(',0.0') 
        if neo_category_group_distribute.has_key(values['neo_category_group_id']):
            fo.write(',' + str(neo_category_group_distribute[values['neo_category_group_id']]))
        else:
            fo.write(',0.0') 
        fo.write(',' + str(values['click_count']) + '\n')
fo.close() 

