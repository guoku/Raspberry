import datetime
import MySQLdb
import pymongo

client = pymongo.Connection('localhost', 27017)
db = client['mango']
item_coll = db['item']


conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")
cur_gk.execute("select id from base_entity where title is NULL or title=''")
entity_without_price_list = [] 
for row in cur_gk.fetchall():
    print id




