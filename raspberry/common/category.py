# coding=utf8
from models import Category_Group as RBCategoryGroupModel
from models import Category as RBCategoryModel
import datetime 

class RBCategory(object):
    
    @staticmethod
    def all_list():
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
    
    @staticmethod
    def all_dict():
        _dict = {} 
        for _cat_obj in RBCategoryModel.objects.order_by('id'):
            _dict[_cat_obj.id] = {
                'title' : _cat_obj.title,
                'pid' : _cat_obj.pid
            }
        return _dict
    
    @staticmethod
    def get(category_id):
        _obj = RBCategoryModel.objects.get(pk = category_id)
        return {
            'id' : _obj.id,
            'title' : _obj.title,
            'group_id' : _obj.group_id,
            'status' : _obj.status
        }
        
    
    @staticmethod
    def find(group_id = None):
        if group_id != None: 
            _hdl = RBCategoryModel.objects.filter(group_id = group_id)
        else:
            _hdl = RBCategoryModel.objects.all()
        _rslt = []
        for _cat_obj in _hdl:
            _rslt.append({
                'id' : _cat_obj.id,
                'title' : _cat_obj.title,
                'group_id' : _cat_obj.group_id,
                'status' : _cat_obj.status
            })
        return _rslt
            
    @staticmethod
    def allgroups():
        _rslt = []
        for _group_obj in RBCategoryGroupModel.objects.all():
            _rslt.append({
                'id' : _group_obj.id,
                'title' : _group_obj.title,
                'status' : _group_obj.status
            })
        return _rslt

