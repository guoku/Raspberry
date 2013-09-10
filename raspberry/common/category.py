# coding=utf8
from models import Category as RBCategoryModel
import datetime 

class RBCategory(object):
    
    @staticmethod
    def all():
        _dict = {} 
        _list = []
        for _cat_obj in RBCategoryModel.objects.order_by('id'):
            _dict[_cat_obj.id] = _cat_obj.title
            if _cat_obj.pid != _cat_obj.id:
                _ttl = _dict[_cat_obj.pid] + '-'  + _cat_obj.title
            else:
                _ttl = _cat_obj.title
            _list.append({
                'id' : _cat_obj.id, 
                'title' : _ttl
            })
        return _list
    
