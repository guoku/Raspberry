# coding=utf8
from django.conf import settings
from models import Image as ImageModel
from hashlib import md5
from pymogile import Client
from wand.image import Image as WandImage
import datetime

class Image(object):
    
    class Figure(object):
        
        def __init__(self, key):
            self.__key = key 
            self.__origin_store_key = 'entity/origin/' + self.__key
            self.__datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
        
        def get_hash_key(self):
            return self.__key
    
        def __crop_square(self, data):
            _img = WandImage(blob = data)
            _delta = _img.width - _img.height
            if _delta > 0:
                _img.crop(_delta / 2 , 0, width = _img.height, height = _img.height)
            elif _delta < 0:
                _img.crop(0, -_delta / 2, width = _img.width, height = _img.width)
            return _img.make_blob()
        
        def __resize(self, data, w, h):
            _img = WandImage(blob = data)
            _img.resize(w, h)
            return _img.make_blob()
        
        @classmethod
        def create(cls, origin_data):
            _key = md5(origin_data).hexdigest()
            _inst = cls(_key)
            
            if len(_inst.__datastore.get_paths(_inst.__origin_store_key)) == 0:
                _inst.write(origin_data)
    
            return _inst
    
        def read_origin_link(self):
            return settings.IMAGE_SERVER + self.__origin_store_key
    
        def write(self, origin_data): 
            _square_data = self.__crop_square(origin_data)
            _clean_data = self.__resize(_square_data, 310, 310)
            _fp = self.__datastore.new_file(self.__origin_store_key)
            _fp.write(_clean_data)
            _fp.close()
    
    def __init__(self, image_id):
        self.image_id = image_id 
    
    def __ensure_image_obj(self):
        if not hasattr(self, 'image_obj'):
            self.image_obj = ImageModel.objects.filter(id = self.image_id).first()
    
    @classmethod
    def create(cls, source, origin_url = None, image_data = None):
        if origin_url != None:
            _image_id = Image.get_image_id_by_origin_url(origin_url)
            if _image_id != None:
                return cls(_image_id)
        elif image_data != None:
            _figure = cls.Figure.create(image_data)
            _store_hash = _figure.get_hash_key()
            _image_id = Image.get_image_id_by_store_hash(_store_hash)
            if _image_id != None:
                return cls(_image_id)
        
        _store_hash = None 
        _image_obj = ImageModel( 
            source = source, 
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        if origin_url != None:
            _image_obj.origin_url = origin_url
        if _store_hash != None:
            _image_obj.store_hash = _store_hash 

        _image_obj.save()

        _inst = cls(str(_image_obj.id))
        _inst.image_obj = _image_obj
        return _inst
    
    @classmethod
    def get_image_id_by_store_hash(cls, store_hash):
        if store_hash != None:
            _image_obj = ImageModel.objects.filter(store_hash = store_hash).first()
            if _image_obj != None:
                return str(_image_obj.id)
        return None
    
    @classmethod
    def get_image_id_by_origin_url(cls, origin_url):
        if origin_url != None:
            _image_obj = ImageModel.objects.filter(origin_url = origin_url).first()
            if _image_obj != None:
                return str(_image_obj.id)
        return None
        

    def read(self):
        self.__ensure_image_obj()
        _context = {}
        _context["source"] = self.image_obj.source
        _context["origin_url"] = self.image_obj.origin_url
        return _context

    def getlink(self):
        self.__ensure_image_obj()
        if self.image_obj.store_hash != None:
            _link = self.Figure(self.image_obj.store_hash).read_origin_link()
        elif self.image_obj.origin_url != None:
            _link = self.image_obj.origin_url
        else:
            _link = None
        return _link
