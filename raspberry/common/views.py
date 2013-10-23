# coding=utf-8
from django.conf import settings
from django.http import HttpResponse
from pymogile import Client, MogileFSError
from avatar import Avatar
from entity import RBEntity 

def local_image(request, key):
    _data = Avatar.read_image_data_by_store_key(key)
    return HttpResponse(_data, content_type = "image/jpeg")
        
