import pymongo
import MySQLdb

conn = pymongo.Connection('localhost', 27017)
db = conn.experiment


def dump_by_time_detail():
    fo = open('guoku_logging_12_31.txt', 'w')
    count = 0
    for doc in db.logging.find():
        fo.write('%s\t%s\t%s\n'%(doc['entity_id'], doc['item_id'], doc['logged_time']))
        count += 1
        if count % 10000 == 0:
            print '%d lines processed...'%count
    
    fo.close()

def dump_by_time_aggressed_by_hour():
    fo = open('guoku_logging_12_31_hour.txt', 'w')
    count = 0
    time_interval = None
    jump_count = 0
    for doc in db.logging.find():
        current_time_interval = str(doc['logged_time'].year) + '-' + str(doc['logged_time'].month) + '-' + str(doc['logged_time'].day) + '-' + str(doc['logged_time'].hour)

        if current_time_interval != time_interval:
            if time_interval != None:
                fo.write('%s\t%d\n'%(time_interval, jump_count))
            time_interval = current_time_interval
            jump_count = 0
        jump_count += 1
        count += 1
        if count % 10000 == 0:
            print '%d lines processed...'%count
    
    fo.close()

def dump_into_mysql():
    conn_experiment=MySQLdb.Connection("localhost", "root", "123456", "experiment")
    cur=conn_experiment.cursor()
    cur.execute("SET names utf8")
    count=0
    for doc in db.logging.find():
        entity_id=doc['entity_id']
        item_id=doc['item_id']
        year=doc['logged_time'].year
        month=doc['logged_time'].month
        date=doc['logged_time'].day
        hour=doc['logged_time'].hour
        wday=doc['logged_time'].weekday()
         
        sql_query="INSERT INTO log_data_detail (entity_id, item_id, year, month, date, hour, wday) VALUES (%d, '%s', %d, %d, %d, %d, %d);"%(entity_id, item_id, year, month, date, hour, wday)

        cur.execute(sql_query)

        count+=1
        if count % 10000 == 0:
            print '%d lines processed...'%count
            conn_experiment.commit()
    conn_experiment.commit()
    

dump_into_mysql()