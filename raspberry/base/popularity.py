# coding=utf-8
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import Count 
import datetime, time
import random 

from models import Entity_Like 


################# Popular Entity ###############################3

def _generate_popular_entity_to_cache(scale = 'daily'):
    
    _start = datetime.datetime.now()
    if scale == "monthly":
        _t_delta = datetime.timedelta(hours = 720) 
    elif scale == "weekly":
        _t_delta = datetime.timedelta(hours = 168) 
    else:
        _t_delta = datetime.timedelta(hours = 24) 
    _cache_key = 'entity_popularity_' + scale
   
    _results = Entity_Like.objects.filter( 
        created_time__gt = datetime.datetime.now() - _t_delta, 
        created_time__lt = datetime.datetime.now() 
    ).values("entity").annotate(like_count = Count("entity")).order_by("-like_count")

    _context = {}
    _context["updated_time"] = datetime.datetime.now()
    _context["data"] = [] 
    for _row in _results[0:100]:
        _context["data"].append([_row['entity'], _row['like_count']])
    
    cache.set(_cache_key, _context, 864000)
    return _context 


def generate_popular_entity():
    _generate_popular_entity_to_cache(scale = 'daily')
    _generate_popular_entity_to_cache(scale = 'weekly')
    _generate_popular_entity_to_cache(scale = 'monthly')

def read_popular_entity_to_cache(scale = 'daily', json = False):
    _cache_key = 'entity_popularity_' + scale
    _context = cache.get(_cache_key)
    if _context == None:
        return None
    else:  
        if json:
            _context['updated_time'] = time.mktime(datetime.datetime.now().timetuple())
        return _context

