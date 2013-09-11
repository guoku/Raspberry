from django.conf import settings
from utils.http import JSONResponseParser
import httplib, urllib
import requests

class MangoApiClient(object):
    
    def __init__(self):
        self.__host = settings.MANGO['host'] 
        self.__port = settings.MANGO['port']

    def check_taobao_item_exist(self, taobao_id):
        _url = 'http://%s:%s/taobao/item/check/%s/'%(self.__host, self.__port, taobao_id) 

        _response = requests.get(_url) 
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            if _data["exist"] == 1:
                return _data["entity_id"]
            else:
                return None
        else:
            raise Exception(_parser.message()) 

        
    def create_entity_by_taobao_item(self, taobao_id, **kwargs):
        _url = 'http://%s:%s/entity/create/'%(self.__host, self.__port)
        _data_dict = {
            'taobao_id' : taobao_id,
            'cid' : kwargs['cid'].encode('utf-8'),
            'taobao_title' : kwargs['taobao_title'].encode('utf-8'),
            'taobao_shop_nick' : kwargs['taobao_shop_nick'].encode('utf-8'),
            'taobao_price' : kwargs['taobao_price'].encode('utf-8'),
            'taobao_soldout' : kwargs['taobao_soldout'].encode('utf-8'),
        }
        if kwargs.has_key('brand'):
            _data_dict['brand'] = kwargs['brand'].encode('utf-8')
        if kwargs.has_key('title'):
            _data_dict['title'] = kwargs['title'].encode('utf-8')
        _data = urllib.urlencode(_data_dict)
        _response = requests.post(_url, data = _data)
        
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            return _data["entity_id"]
        else:
            raise Exception(_parser.message()) 


    def read_entity(self, entity_id):
        _url = 'http://%s:%s/entity/%s/'%(self.__host, self.__port, entity_id) 
        _response = requests.get(_url)
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            return _data["context"]
        else:
            raise Exception(_parser.message()) 
         
         
    def read_entities(self, entity_id_list):
        _url = 'http://%s:%s/entity/'%(self.__host, self.__port)
        _params = '&'.join(map(lambda x: 'eid=' + str(x), entity_id_list)) 
        _response = requests.get(_url, params = _params)
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            return _data
        else:
            raise Exception(_parser.message()) 
         
         
    def read_items(self, item_id_list):
        _url = 'http://%s:%s/item/'%(self.__host, self.__port)
        _params = '&'.join(map(lambda x: 'iid=' + str(x), item_id_list)) 
        _response = requests.get(_url, params = _params)
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            return _data
        else:
            raise Exception(_parser.message()) 
         
         
