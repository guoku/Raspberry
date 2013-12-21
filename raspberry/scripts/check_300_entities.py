import datetime
import MySQLdb
import pymongo

client = pymongo.Connection('localhost', 27017)
db = client['guoku']
item_coll = db['item']


conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_12_12")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")

mapping = {}
cur_gk.execute("select taobao_category_id, neo_category_id from base_taobao_item_neo_category_mapping")
for row in cur_gk.fetchall():
    mapping[row[0]] = row[1]

cur_gk.execute("select id from base_entity where neo_category_id=300")
for row in cur_gk.fetchall():
    entity_id = row[0]
    neo_category_id = 300
    for doc in item_coll.find({"entity_id" : entity_id}):
        cid = doc['cid']
        if mapping.has_key(cid):
            print "UPDATE base_entity SET neo_category_id=%s WHERE id=%d;"%(mapping[cid], entity_id)
            break
    



