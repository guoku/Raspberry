import MySQLdb
import pymongo
import datetime



def load_price_distribute():
    conn = MySQLdb.Connection("localhost", "root", "123456", "experiment")
    cur = conn.cursor()
    cur.execute("SET names utf8")
    
    sql_query = "select floor from guoku_price_distribute where floor > 0 order by floor desc"
    cur.execute(sql_query)
    price_distribute = []
    for row in cur.fetchall():
        price_distribute.append(float(row[0]))
    conn.commit()
    conn.close()
    return price_distribute 

def load_entity_info():
    conn = MySQLdb.Connection("localhost", "root", "123456", "guoku")
    cur = conn.cursor()
    cur.execute("SET names utf8")
#    sql_query = "select base_entity.id, base_note.post_time, price, base_entity.category_id, base_category.pid, base_entity.neo_category_id, base_neo_category.group_id from base_entity inner join base_note on base_entity.id=base_note.entity_id inner join base_category on base_entity.category_id=base_category.id inner join base_neo_category on base_entity.neo_category_id=base_neo_category.id;"
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
entity_dict = load_entity_info()

fo = open('guoku_click_log_all.arff', 'w')
fo.write('@relation guoku_click_log_all\n\n') 

fo.write('@attribute price NUMERIC\n')
for i in range(1, 13):
    fo.write('@attribute is_c%d {0,1}\n'%i)
for i in range(1, 42):
    fo.write('@attribute is_nc%d {0,1}\n'%i)
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
                    if doc['logged_time'] - entity_dict[entity_id]['post_time'] < datetime.timedelta(hours=48):
                        entity_dict[entity_id]['click_count'] += 1
    except Exception, e:
        print e
    i += 1
    if i % 100000 == 0:
        print "%d logs processed..."%i


stat = {}
price_stat = {}
for entity_id, values in entity_dict.items():
    if values['click_count'] > 0:
        fo.write(str(set_price_value(values['price'], price_distribute)))
        for i in range(1, 13):
            if values['category_parent_id'] == i:
                fo.write(',1')
            else:
                fo.write(',0')
        for i in range(1, 42):
            if values['neo_category_group_id'] == i:
                fo.write(',1')
            else:
                fo.write(',0')
        fo.write(',' + str(values['click_count']) + '\n')
        
        if not stat.has_key(values['click_count']):
            stat[values['click_count']] = 0
        stat[values['click_count']] += 1
        
        if not price_stat.has_key(int(values['price'])):
            price_stat[int(values['price'])] = 0
        price_stat[int(values['price'])] += values['click_count'] 
#    else:
#        fo.write('alert: %d\n'%entity_id)
        
fo.close() 


for item in sorted(price_stat.items()):
    print "%d\t%d"%(item[0], item[1])
