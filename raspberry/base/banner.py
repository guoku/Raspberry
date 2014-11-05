# coding=utf8
from django.http import Http404
from django.utils.log import getLogger
from models import Banner as BannerModel
from django.conf import settings
from django.core.cache import cache

from image import Image
import datetime
import urllib
import random 
import time

log = getLogger('django')



class Banner(object):
    
    def __init__(self, banner_id):
        self.banner_id = int(banner_id)
   
    def read(self):

        try:
            _obj = BannerModel.objects.get(pk = self.banner_id)
        except BannerModel.DoesNotExist, e:
            log.error("Error: %s" % e.message)
            raise Http404
        return {
            'banner_id' : _obj.id,
            'image' : Image(_obj.image).getlink(),
            'key' : _obj.key,
            'content_type' : _obj.content_type,
            'weight' : _obj.weight
        }

        

    @classmethod
    def create(cls, key, content_type, image_data, weight = 0):
        _image_obj = Image.create(
            source = 'banner', 
            image_data = image_data,
            save_in_origin = True
        )
        
        _banner_obj = BannerModel.objects.create(
            content_type = content_type,
            key = key,
            image = _image_obj.image_id,
            weight = weight
        )
        

        return _banner_obj.id
    
    def update(self, weight):
        _obj = BannerModel.objects.get(pk = self.banner_id)
        _obj.weight = int(weight)
        _obj.save()
    
    
    def delete(self):
        _obj = BannerModel.objects.get(pk = self.banner_id)
        _obj.delete()

    @classmethod
    def find(cls, offset = None, count = None, status = None):
        _hdl = BannerModel.objects.all()
        _hdl = _hdl.order_by('-weight')
        if status == 'active':
            _hdl = _hdl.filter(weight__gt = 0)
        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]    
        _banner_context_list = []
        for _obj in _hdl:
            if _obj.content_type == 'entity':
                _url = 'guoku://entity/%s'%(_obj.key)
            elif _obj.content_type == 'user':
                _url = 'guoku://user/%s'%(_obj.key)
            elif _obj.content_type == 'user_tag':
                _tokens = _obj.key.split(':')
                _user_id = _tokens[0]
                _tag = _tokens[1]
                _url = 'guoku://user/%s/tag/%s'%(_user_id, urllib.quote(_tag.encode('utf-8')))
            elif _obj.content_type == 'category':
                _url = 'guoku://category/%s'%(_obj.key)
            else:
                _url = _obj.key 
                
                
            _banner_context_list.append({
                'banner_id' : _obj.id,
                'url' : _url,
                'image' : Image(_obj.image).getlink(),
                'key' : _obj.key,
                'content_type' : _obj.content_type,
                'weight' : _obj.weight,
                'web_url': _obj.web_url,
            })

        return _banner_context_list
    
