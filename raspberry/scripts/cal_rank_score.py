import datetime
import MySQLdb


category_distribute = {} 
def load_category_distribute():
    fi = open("../../experiment/factor/category.fct", "r")
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        category_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()

category_parent_distribute = {} 
def load_category_parent_distribute():
    fi = open("../../experiment/factor/category_parent.fct", "r")
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        category_parent_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()

neo_category_group_distribute = {} 
def load_neo_category_group_distribute():
    fi = open("../../experiment/factor/neo_category_group.fct", "r")
    for line in fi.readlines():
        tokens = line.strip().split('\t')
        neo_category_group_distribute[int(tokens[0])] = float(tokens[3])
    fi.close()

def price_normalize(price):
    if price == 0.00:
        return 0.0
    if price <= 16.00:
        return 0.1
    if price <= 35.00:
        return 0.2
    if price <= 59.00:
        return 0.3
    if price <= 90.00:
        return 0.4 
    if price <= 140.00:
        return 0.5
    if price <= 200.00:
        return 0.6
    if price <= 304.00:
        return 0.7
    if price <= 495.00:
        return 0.8
    if price <= 999.00:
        return 0.9
    return 1.0


def cal_rank_score(price, category_id, category_parent_id, neo_category_group_id): 
    value = -75.5563 * price_normalize(price) - 85.0271 
    if category_distribute.has_key(category_id):
        value += 2.1169 * category_distribute[category_id]
    if category_parent_distribute.has_key(category_parent_id):
        value += 2.1753 * category_parent_distribute[category_parent_id]
    if neo_category_group_distribute.has_key(neo_category_group_id):
        value += 0.6261 * neo_category_group_distribute[neo_category_group_id]

    return value


load_category_parent_distribute()
load_neo_category_group_distribute()
conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_02_11")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")


count = 0
cur_gk.execute("select base_entity.id, base_entity.price, base_entity.category_id, base_category.pid, base_neo_category.group_id from base_entity inner join base_category on base_entity.category_id=base_category.id inner join base_neo_category on base_entity.neo_category_id=base_neo_category.id") 
for row in cur_gk.fetchall():
    rank_score = cal_rank_score(row[1], row[2], row[3], row[4])
    sql_query = "update base_entity set rank_score=%d where id=%d;"%(int(rank_score), row[0]) 
    cur_gk.execute(sql_query)
    
    count += 1
    if count % 100000 == 0:
        print "%d lines processed..."%count
conn_gk.commit()
