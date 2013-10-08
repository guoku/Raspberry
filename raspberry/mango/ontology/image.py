# coding=utf8
from models import Image as ImageModel
import datetime

class Image(object):
    
    def __init__(self, image_id):
        self.__image_id = image_id 
    
    def get_image_id(self):
        return self.__image_id
    
    def __ensure_image_obj(self):
        if not hasattr(self, '__image_obj'):
            self.__image_obj = ImageModel.objects.filter(id = self.__image_obj).first()
    
    @classmethod
    def create(cls, source, origin_url): 
        _image_obj = ImageModel( 
            source = source, 
            origin_url = origin_url,
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now() 
        )
        _image_obj.save()

        _inst = cls(str(_image_obj.id))
        _inst.__image_obj = _image_obj
        return _inst

    def read(self):
        self.__ensure_image_obj()
        _context = {}
        _context["source"] = self.__image_obj.source
        _context["origin_url"] = self.__image_obj.origin_url
        return _context    
