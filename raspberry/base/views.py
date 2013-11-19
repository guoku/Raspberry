# coding=utf-8
from django.conf import settings
from django.http import HttpResponse
from pymogile import Client, MogileFSError
from avatar import Avatar
from entity import Entity 

def local_avatar_image(request, size, key):
    _data = Avatar.read_image_data_by_store_key('avatar/' + size + '/' + key)
    return HttpResponse(_data, content_type = "image/jpeg")
        
def local_entity_image(request, key, image_format):
    _data = Avatar.read_image_data_by_store_key('entity/' + key + '.' + image_format)
    return HttpResponse(_data, content_type = "image/jpeg")
        
def local_entity_image_extend(request, key1, key2, key3):
    _data = Avatar.read_image_data_by_store_key('entity/' + key1 + '.' + key2 + '.' + key3)
    return HttpResponse(_data, content_type = "image/jpeg")
        
