import datetime
import MySQLdb
import pymongo

client = pymongo.Connection('localhost', 27017)
db = client['guoku']
image_coll = db['image']

dic = {}
for doc in image_coll.find({ "origin_url" : { '$regex' : '._b\.jpg' }}):
    dic[doc['_id']] = doc['origin_url'].replace('_b.jpg', '')

print "%d image found..."%(len(dic))
count = 0
for _id, image_url in dic.items():
    image_coll.update({ '_id' : _id }, { '$set' : { 'origin_url' : image_url }})
    count += 1
    if count % 1000 == 0:
        print "%d image fixed..."%count
