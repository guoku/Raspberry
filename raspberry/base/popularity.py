# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import Count 
import datetime, time
import random 

from models import Entity_Like 


################# Popular Entity ###############################3

def get_popular_entity(scale = 'daily', json = False):
    
    if scale == "monthly":
        t_delta = datetime.timedelta(hours = 720) 
    elif scale == "weekly":
        t_delta = datetime.timedelta(hours = 168) 
    else:
        t_delta = datetime.timedelta(hours = 24) 
    
    _results = Entity_Like.objects.filter( 
        created_time__gt = datetime.datetime.now() - t_delta, 
        created_time__lt = datetime.datetime.now() 
    ).values("entity").annotate(like_count = Count("entity")).order_by("-like_count")

    _context = {}
    if json:
        _context['updated_time'] = time.mktime(datetime.datetime.now().timetuple())
    else:
        _context["updated_time"] = datetime.datetime.now()
    _context["data"] = [] 
    for _row in _results:
        _context["data"].append([_row['entity'], _row['like_count']])
    
    return _context 

