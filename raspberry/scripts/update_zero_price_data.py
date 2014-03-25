import MySQLdb
import pymongo

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_02_11")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")

cur_gk.execute("select id from base_entity where price=0")
entity_list = []
for row in cur_gk.fetchall():
    entity_id = row[0]
    entity_list.append(entity_id)

conn = pymongo.Connection(host='localhost', port=27017)
db = conn.guoku
col = db.item

update_count = 0
cur_count = 0
tot_count = len(entity_list)
for entity_id in entity_list:
    price = None
    for item in col.find({"entity_id" : entity_id}):
        if price == None or item['price'] < price:
            price = item['price']
    
    if price != None:
        sql_query = "UPDATE base_entity SET price=%f WHERE id=%d;"%(price, entity_id)
        cur_gk.execute(sql_query)
        update_count += 1
    cur_count += 1
    if cur_count % 1000 == 0:
        print "[%d / %d / %d] processed..."%(cur_count, update_count, tot_count)
        conn_gk.commit()

         
conn_gk.commit()
