import pymongo

conn = pymongo.Connection(host='localhost', port=27017)
db = conn.guoku

count = 0
for image in db.image.find({"origin_url":{"$regex": "_b.jpg"}}):
    try:
        origin_url = image['origin_url']
        origin_url_new = origin_url.replace("_b.jpg", "")
        image['origin_url'] = origin_url_new
        db.image.update({"_id": image['_id']}, {"$set":{"origin_url":origin_url_new}})
    except Exception, e:
        print e
    count +=1
    if count % 1000 == 0:
        print "%d images processed..."%count


