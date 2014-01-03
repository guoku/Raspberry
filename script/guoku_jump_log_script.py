import datetime
import MySQLdb
import pymongo

conn = pymongo.Connection('localhost', 27017)
db = conn.guoku

item_dict = {}
count = 0
start_time = None
end_time = None
for doc in db.logging_backup.find():
    try:
        if doc.has_key('item_id'):
            if not item_dict.has_key(doc['item_id']):
                item_dict[doc['item_id']] = {
                    'entity_id' : doc['entity_id'],
                    'count' : 0
                }
            item_dict[doc['item_id']]['count'] += 1
        
        count += 1
        if start_time == None or doc['logged_time'] < start_time:
            start_time = doc['logged_time']
        if end_time == None or doc['logged_time'] > start_time:
            end_time = doc['logged_time']
        if count % 1000 == 0:
            print '%d processed..'%count
    except Exception, e:
        print e

items_sorted = sorted(item_dict.items(), key = lambda x : x[1]['count'], reverse = True)
fo = open('output.txt', 'w')
for item in items_sorted:
    fo.write("%d\t%d\t%d\n"%(item[1]['entity_id'], item[0], item[1]['count']))
fo.close()
print "from [%s]\n to [%s]"%(start_time, end_time)
