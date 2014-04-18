import pymongo
import MySQLdb
import datetime

conn = pymongo.Connection('localhost', 27017)
db = conn.experiment
    
entity_dict = {}

def load_entity_info():
    conn = MySQLdb.Connection("localhost", "root", "123456", "guoku")
    cur = conn.cursor()
    cur.execute("SET names utf8")
    sql_query="select base_entity.id, base_note.post_time, price, base_entity.category_id, base_category.pid, base_entity.neo_category_id, base_neo_category.group_id from base_entity inner join base_note on base_entity.id=base_note.entity_id inner join base_category on base_entity.category_id=base_category.id inner join base_neo_category on base_entity.neo_category_id=base_neo_category.id;"
    cur.execute(sql_query)
    count = 0
    for row in cur.fetchall():
        entity_dict[row[0]] = {
            'post_time': row[1],
            'price': row[2],
            'category_id': row[3],
            'category_parent_id': row[4],
            'neo_category_id': row[5],
            'neo_category_group_id': row[6],
        }
        count += 1
        if count % 10000 == 0:
            print "%d entities loaded..."%count
    conn.commit()
            


def dump_into_mysql():
    conn_experiment = MySQLdb.Connection("localhost", "root", "123456", "experiment")
    cur = conn_experiment.cursor()
    cur.execute("SET names utf8")
    count = 0
    err_count = 0
    cur.execute('delete from guoku_log_detail')
    for doc in db.log_2013.find():
        try:
            entity_id =  doc['entity_id']
            item_id =  doc['item_id']
            year =  doc['logged_time'].year
            month =  doc['logged_time'].month
            date =  doc['logged_time'].day
            hour =  doc['logged_time'].hour
            wday =  doc['logged_time'].weekday()
            gap_hour = -1
            if entity_dict[entity_id]['post_time'] != None:
                gap = doc['logged_time'] - entity_dict[entity_id]['post_time']
                gap_hour = gap.days * 24 + gap.seconds / 3600
            
            sql_query="INSERT INTO guoku_log_detail (entity_id, price, category_id, category_parent_id, neo_category_id, neo_category_group_id, item_id, year, month, date, hour, wday, gap_hour) VALUES (%d, %f, %d, %d, %d, %d, '%s', %d, %d, %d, %d, %d, %d);"%(entity_id, entity_dict[entity_id]['price'], entity_dict[entity_id]['category_id'], entity_dict[entity_id]['category_parent_id'], entity_dict[entity_id]['neo_category_id'], entity_dict[entity_id]['neo_category_group_id'], item_id, year, month, date, hour, wday, gap_hour)
            
            cur.execute(sql_query)
            
            count += 1
            if count % 10000 == 0:
                print '%d:%d lines processed...'%(count, err_count)
                conn_experiment.commit()
        except Exception, e:
            err_count += 1
            pass 
    conn_experiment.commit()
    
load_entity_info()
dump_into_mysql()


#CREATE TABLE `guoku_log_detail` (
#`id` int(11) NOT NULL AUTO_INCREMENT,
#`entity_id` int(11) DEFAULT NULL,
#`price` decimal(20,2) NOT NULL,
#`category_id` int(11) DEFAULT NULL,
#`category_parent_id` int(11) DEFAULT NULL,
#`neo_category_id` int(11) DEFAULT NULL,
#`neo_category_group_id` int(11) DEFAULT NULL,
#`item_id` varchar(32) DEFAULT '', 
#`year` int(11) NOT NULL,
#`month` int(11) NOT NULL,
#`date` int(11) NOT NULL,
#`wday` int(11) NOT NULL,
#`hour` int(11) NOT NULL,
#`gap_hour` int(11) NOT NULL,
#PRIMARY KEY (`id`),
#KEY `entity_price` (`price`),
#KEY `entity_category_id` (`category_id`),
#KEY `entity_category_parent_id` (`category_parent_id`),
#KEY `entity_neo_category_id` (`neo_category_id`),
#KEY `entity_neo_category_group_id` (`neo_category_group_id`)
#) ENGINE=InnoDB DEFAULT CHARSET=utf8;

