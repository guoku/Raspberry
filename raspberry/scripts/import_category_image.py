# coding=utf8
import datetime
import MySQLdb
import os


#alter table common_category add column `image_store_hash` varchar(64) DEFAULT NULL;
#alter table common_category add KEY `common_category_f192161f` (`image_store_hash`);

conn = MySQLdb.Connection('localhost', 'root', '123456', 'guoku_11_21')
cur = conn.cursor()
cur.execute("SET names utf8")


cur.execute("SELECT id, title from base_neo_category;")
categories = {}
for row in cur.fetchall():
    title = row[1].replace('/', '')
    categories[title] = {
        'category_id' : row[0]
    }

image_path = '../../../data/11.3icon'
for root, dirs, files in os.walk(image_path):
    for f in files:
        if '@2x.png' in f:
            title = f.replace('@2x.png', '')
            title = title.replace(' ', '')
            if not categories.has_key(title):
                print title
            else:
                categories[title]['large'] = f
        else:
            title = f.replace('.png', '')
            title = title.replace(' ', '/')
            if not categories.has_key(title):
                print title
            else:
                categories[title]['small'] = f


from pymogile import Client
from hashlib import md5
datastore = Client(
    domain = 'staging', 
    trackers = ['10.0.1.23:7001']
)
for title, obj in categories.items():
    if obj.has_key('large') and obj.has_key('small'):
        f = open(image_path + '/' + obj['large'], 'r')
        large_data = f.read()
        f.close()
        key = md5(large_data).hexdigest()
        
        f = open(image_path + '/' + obj['small'], 'r')
        small_data = f.read()
        f.close()
        
        mgf = datastore.new_file('category/large/' + key)
        mgf.write(large_data)
        mgf.close() 
        
        mgf = datastore.new_file('category/small/' + key)
        mgf.write(small_data)
        mgf.close()
        
        
        cur.execute("UPDATE base_neo_category set image_store_hash='%s' WHERE id=%d;"%(key, obj['category_id'])) 
        print "%s created...[%s]"%(title, key)
        
f = open(image_path + '/?@2x.png', 'r')
large_data = f.read()
f.close()
key = md5(large_data).hexdigest()

f = open(image_path + '/?.png', 'r')
small_data = f.read()
f.close()
        
mgf = datastore.new_file('category/large/' + key)
mgf.write(large_data)
mgf.close() 

mgf = datastore.new_file('category/small/' + key)
mgf.write(small_data)
mgf.close()

print "unkonw key is: [%s]"%key
        

conn.commit()

