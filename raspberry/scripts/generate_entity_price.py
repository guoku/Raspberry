import datetime

import pymongo
client = pymongo.Connection('localhost', 27017)
db = client['mango']
entity_coll = db['entity']
item_coll = db['item']

_dict = {}
for _entity in entity_coll.find():
    _entity_id = str(_entity['_id'])
    _price = None
    for _item in item_coll.find({ "entity_id" : _entity_id }):
        _item_price = _item['price']
        if _price == None or _item_price < _price:
            _price = _item_price
    if _price == None:
        print str(_entity['_id'])
        _price = 0.5
    
    _dict[_entity_id] = _price


from bson.objectid import ObjectId
for key, value in _dict.items():
    print "%s\t%s"%(key, value)
    entity_coll.update({ "_id" : ObjectId(key) }, { "$set" : { "price" : value }})

