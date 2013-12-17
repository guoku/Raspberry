# coding=utf-8
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import Count 
import datetime, time
import random 

from category import Category
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
    #_generate_popular_entity_to_cache(scale = 'monthly')

def read_popular_entity_from_cache(scale = 'daily', json = False):
    _cache_key = 'entity_popularity_' + scale
    _context = cache.get(_cache_key)
    if _context == None:
        return None
    else:  
        if json:
            _context['updated_time'] = time.mktime(datetime.datetime.now().timetuple())
        return _context


################# Popular Category ###############################3

def generate_popular_category_to_cache():
    
    _cache_key = 'category_popularity_24hours'
#    _start_time = datetime.datetime(2013, 12, 9, 16, 0, 0) 
    _start_time = datetime.datetime.now()
    _t_delta = datetime.timedelta(hours = 1) 
    _results = Entity_Like.objects.filter( 
        created_time__gt = _start_time  - _t_delta, 
        created_time__lt = _start_time 
    ).values('entity__category').annotate(like_count = Count("entity__category")).order_by("-like_count")

    _context = {}
    _context["updated_time"] = datetime.datetime.now()
    _context["data"] = [] 
    for _row in _results[0:20]:
        _category_id = _row['entity__category']
        _context['data'].append(Category(_category_id).read())
    
    cache.set(_cache_key, _context, 600)
    return _context 


def read_popular_category(json = False):
    _cache_key = 'category_popularity_24hours'
    _context = cache.get(_cache_key)
    if _context == None:
        _context = generate_popular_category_to_cache() 
    if json:
        _context['updated_time'] = time.mktime(datetime.datetime.now().timetuple())
    return _context

