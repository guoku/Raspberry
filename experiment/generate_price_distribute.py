import pymongo
import MySQLdb
import datetime

def cal_price_distribute():
    conn = MySQLdb.Connection("localhost", "root", "123456", "guoku")
    cur = conn.cursor()
    cur.execute("SET names utf8")
    
    sql_query = "select base_entity.price from base_entity inner join base_note on base_entity.id=base_note.entity_id where base_note.post_time is not null" 
    cur.execute(sql_query)
    price_dict = {}
    count = 0
    for row in cur.fetchall():
        price = row[0]
        if not price_dict.has_key(price):
            price_dict[price] = 0
        price_dict[price] += 1
    
        count += 1
        if count % 10000 == 0:
            print "%d lines processed..."%count
    
    conn.commit()
    conn.close()
    return sorted(price_dict.items())

def insert_price_distribute(price_distribute_list, tier_count=10):
    conn = MySQLdb.Connection("localhost", "root", "123456", "experiment")
    cur = conn.cursor()
    cur.execute("SET names utf8;")
    cur.execute("DELETE FROM guoku_price_distribute;")
    
    item_count_total = 0
    for price_vector in price_distribute_list:
        item_count_total += price_vector[1]
    
    item_count_for_one_tier = item_count_total / tier_count
    
    floor = 0.0
    j = 1
    counting = 0
    for item in price_distribute_list:
        counting += item[1] 
        if counting >= j * item_count_for_one_tier:
            sql_query = "INSERT INTO guoku_price_distribute (floor, ceiling, count) VALUES (%f, %f, %d);"%(floor, item[0], counting)
            cur.execute(sql_query)
            floor = item[0] 
            j += 1
            if j == tier_count:
                break
    sql_query = "INSERT INTO guoku_price_distribute (floor, count) VALUES (%f, %d);"%(floor, item_count_total)
    cur.execute(sql_query)
    conn.commit()
    conn.close()
    

price_distribute_list = cal_price_distribute()
insert_price_distribute(price_distribute_list)

#CREATE TABLE `guoku_price_distribute` (
#`id` int(11) NOT NULL AUTO_INCREMENT,
#`floor` decimal(20,2),
#`ceiling` decimal(20,2), 
#`count` int(11) NOT NULL,
#PRIMARY KEY (`id`)
#) ENGINE=InnoDB DEFAULT CHARSET=utf8;

