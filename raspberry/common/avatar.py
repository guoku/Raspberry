# coding=utf8
from django.conf import settings
from hashlib import md5
from pymogile import Client
from wand.image import Image

class Avatar(object):
    
    def __init__(self, key):
        self.__key = key 
        self.__origin_store_key = 'avatar/origin/' + self.__key
        self.__large_store_key = 'avatar/large/' + self.__key
        self.__small_store_key = 'avatar/small/' + self.__key
   
    def __ensure_datastore_client(self):
        if not hasattr(self, '__entity_obj'):
            self.__datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
    
    def __crop_square(self, data):
        _img = Image(blob = data)
        _delta = _img.width - _img.height
        if _delta > 0:
            _img.crop(_delta / 2 , 0, width = _img.height, height = _img.height)
        elif _delta < 0:
            _img.crop(0, 0, width = _img.width, height = _img.width)
        return _img.make_blob()
    
    def __resize(self, data, w, h):
        _img = Image(blob = data)
        _img.resize(w, h)
        return _img.make_blob()

    def get_hash_key(self):
        return self.__key
   
    @classmethod
    def create(cls, origin_data):
        _key = md5(origin_data).hexdigest()
        _inst = cls(_key)

        _inst.__ensure_datastore_client()
        if len(_inst.__datastore.get_paths(_inst.__origin_store_key)) == 0:
            _inst.write(origin_data)

        return _inst
     
    def read_large_link(self):
        return settings.IMAGE_SERVER + self.__large_store_key
    
    def read_small_link(self):
        return settings.IMAGE_SERVER + self.__small_store_key

    def write(self, origin_data): 
        self.__ensure_datastore_client()
        _square_data = self.__crop_square(origin_data)
         
        _fp = self.__datastore.new_file(self.__origin_store_key)
        _fp.write(origin_data)
        _fp.close()

        _large_data = self.__resize(_square_data, 180, 180)
        _fp = self.__datastore.new_file(self.__large_store_key)
        _fp.write(_large_data)
        _fp.close()
        
         
        _small_data = self.__resize(_square_data, 50, 50)
        _fp = self.__datastore.new_file(self.__small_store_key)
        _fp.write(_small_data)
        _fp.close()
    
    @staticmethod
    def read_image_data_by_store_key(store_key): 
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        return _datastore.get_file_data(store_key)
