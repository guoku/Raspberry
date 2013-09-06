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

        
    def create_entity_by_taobao_item(self, taobao_id, **kwargs):
        _url = 'http://%s:%s/entity/create/'%(self.__host, self.__port) 
        _data_dict = {
            'taobao_id' : taobao_id,
            'taobao_category_id' : kwargs['taobao_category_id'].encode('utf-8'),
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


    def read_entity(self, entity_id):
        _url = 'http://%s:%s/entity/%s/'%(self.__host, self.__port, entity_id) 
        _response = requests.get(_url)
        _parser = JSONResponseParser(_response.text)
        if _parser.success():
            _data = _parser.read()
            return _data["context"]
         
         
