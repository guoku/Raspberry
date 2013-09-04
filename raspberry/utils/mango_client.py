from django.conf import settings
from utils.http import JSONResponseParser
import httplib, urllib
import requests

class MangoApiClient(object):
    def __init__(self):
        pass

    def check_taobao_item(self, taobao_id):
        try:
            _url = 'http://10.0.1.100:8001/taobao/item/check/%s/'%taobao_id 

            _response = requests.get(_url) 
            _parser = JSONResponseParser(_response.text)
            if _parser.success():
                _data = _parser.read()
                if _data["exist"] == 1:
                    return _data["entity_id"]
                else:
                    return None
        except:
            pass

        
    def create_entity_by_taobao_item(self, taobao_id, **kwargs):
        try:
            _url = 'http://10.0.1.100:8001/entity/create/' 
            _data_dict = {
                'taobao_id' : taobao_id,
                'taobao_category_id' : kwargs['taobao_category_id'].encode('utf-8'),
                'taobao_title' : kwargs['taobao_title'].encode('utf-8'),
                'taobao_shop_nick' : kwargs['taobao_shop_nick'].encode('utf-8'),
                'taobao_price' : kwargs['taobao_price'].encode('utf-8'),
                'taobao_soldout' : kwargs['taobao_soldout'].encode('utf-8'),
            }
            if kwargs.has_key('brand'):
                _params_dict['brand'] = kwargs['brand']
            if kwargs.has_key('title'):
                _params_dict['title'] = kwargs['title']
            _data = urllib.urlencode(_data_dict)
            _response = requests.post(_url, data = _data)
            print _response.text
            
            _parser = JSONResponseParser(_response.text)
            if _parser.success():
                _data = _parser.read()
                return _data["entity_id"]


        except:
            pass
         
         
