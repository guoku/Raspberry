import MySQLdb

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_12_09")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")

cur_gk.execute("select entity_id from base_entity where price=0")
entity_list = []
for row in cur_gk.fetchall():
    entity_id = row[0]

