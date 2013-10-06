# coding=utf8
from models import Category_Group as RBCategoryGroupModel
from models import Category as RBCategoryModel
import datetime 

class RBCategory(object):
    
    def __init__(self, category_id):
        self.__category_id= int(category_id)
    
    def __ensure_category_obj(self):
        if not hasattr(self, '__category_obj'):
            self.__category_obj = RBCategoryModel.objects.get(pk = self.__category_id)
    
    def update(self, title = None, group_id = None):
        self.__ensure_category_obj()
        if title != None:
            self.__category_obj.title = title
        if group_id != None:
            self.__category_obj.group_id = group_id 
        self.__category_obj.save()

    
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
                'status' : _group_obj.status,
                'category_count' : RBCategoryModel.objects.filter(group_id = _group_obj.id).count()
            })
        return _rslt

