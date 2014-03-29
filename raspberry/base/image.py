# coding=utf8
from django.conf import settings
from models import Image as ImageModel
from hashlib import md5
from pymogile import Client
from wand.image import Image as WandImage
import datetime

class Image(object):
    
    def __init__(self, image_id):
        self.image_id = image_id 
    
    def __ensure_image_obj(self):
        if not hasattr(self, 'image_obj'):
            self.image_obj = ImageModel.objects.filter(id = self.image_id).first()
    
   
    @classmethod
    def crop_square(cls, data):
        _img = WandImage(blob = data)
        _delta = _img.width - _img.height
        if _delta > 0:
            _img.crop(_delta / 2 , 0, width = _img.height, height = _img.height)
        elif _delta < 0:
            _img.crop(0, -_delta / 2, width = _img.width, height = _img.width)
        return _img.make_blob()
    
    @classmethod
    def resize(cls, data, w, h):
        _img = WandImage(blob = data)
        _img.resize(w, h)
        return _img.make_blob()
    
    @classmethod
    def save_origin_image_data(cls, store_hash, image_data):
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        _fp = _datastore.new_file('img/' + store_hash + '.jpg')
        _fp.write(image_data)
        _fp.close()
    
    @classmethod
    def save_square_image_data_fixed(cls, store_hash, image_data):
        _image_sizes = [240, 310, 480, 640] 
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        
        _square_data = cls.crop_square(image_data)
        _img = WandImage(blob = _square_data)
        if _img.width > 800 or _img.height > 800:
            _square_data = cls.resize(_square_data, 800, 800)
        
        _fp = _datastore.new_file('img/' + store_hash + '.jpg')
        _fp.write(_square_data)
        _fp.close()
        
        for _size in _image_sizes:
            _data_resized = cls.resize(_square_data, _size, _size)
            _fp = _datastore.new_file('img/' + store_hash + '.jpg_' + str(_size) + 'x' + str(_size) + '.jpg')
            _fp.write(_data_resized)
            _fp.close()
    
    @classmethod
    def create(cls, source, origin_url = None, image_data = None, save_in_origin = False):
        if origin_url != None:
            _image_id = Image.get_image_id_by_origin_url(origin_url)
            _store_hash = None
            if _image_id != None:
                return cls(_image_id)
        elif image_data != None:
            _store_hash = md5(image_data).hexdigest()
            if save_in_origin:
                _store_hash = md5(_store_hash + 'GUOKUIMAGESAVEINORIGINSIZE').hexdigest()
                _image_id = Image.get_image_id_by_store_hash(_store_hash)
                if _image_id != None:
                    return cls(_image_id)
                cls.save_origin_image_data(_store_hash, image_data)
            else:
                _store_hash = md5(_store_hash + 'GUOKUIMAGECUTINSQUREANDSAVEINSEVERALSIZES').hexdigest()
                _image_id = Image.get_image_id_by_store_hash(_store_hash)
                if _image_id != None:
                    return cls(_image_id)
                cls.save_square_image_data_fixed(_store_hash, image_data)
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
        if self.image_obj != None:
            if self.image_obj.store_hash != None:
                _link = settings.IMAGE_SERVER + 'img/' + self.image_obj.store_hash + '.jpg'
            elif self.image_obj.origin_url != None:
                _link = self.image_obj.origin_url
            else:
                _link = None
            return _link
        return ''
