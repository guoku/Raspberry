# coding=utf8
from models import Category_Group as RBCategoryGroupModel
from models import Category as RBCategoryModel
from django.conf import settings
import datetime 

DEFAULT_CATEGORY_ICON_KEY = '03717fa531b23c6f5dbd5522e6eec9a1' 
class RBCategory(object):
    
    def __init__(self, category_id):
        self.__category_id= int(category_id)
    
    def __ensure_category_obj(self):
        if not hasattr(self, '__category_obj'):
            self.__category_obj = RBCategoryModel.objects.get(pk = self.__category_id)
    
    def get_category_id(self):
        return self.__category_id
    
    def update(self, title = None, group_id = None):
        self.__ensure_category_obj()
        if title != None:
            self.__category_obj.title = title
        if group_id != None:
            self.__category_obj.group_id = group_id 
        self.__category_obj.save()

    @classmethod
    def create(cls, title, group_id, status = 1):
        _category_obj = RBCategoryModel.objects.create(
            title = title,
            group_id = group_id,
            status = status
        )
        _inst = cls(_category_obj.id)
        _inst.__category_obj = _category_obj
        return _inst
    
    def __load_category_context(self):
        self.__ensure_category_obj()
        _context = {}
        _context['category_id'] = self.__category_obj.id
        _context['category_title'] = self.__category_obj.title
        _context['group_id'] = self.__category_obj.group_id
        _context['status'] = self.__category_obj.status
        if self.__category_obj.image_store_hash:
            _context['category_icon_large'] = settings.IMAGE_SERVER + self.__category_obj.image_store_hash + '_large' 
            _context['category_icon_small'] = settings.IMAGE_SERVER + self.__category_obj.image_store_hash + '_small'
        else:
            _context['category_icon_large'] = settings.IMAGE_SERVER + DEFAULT_CATEGORY_ICON_KEY + '_large' 
            _context['category_icon_small'] = settings.IMAGE_SERVER + DEFAULT_CATEGORY_ICON_KEY + '_small'
        return _context

    
    def read(self):
        return self.__load_category_context()
        
    
    @staticmethod
    def find(group_id = None):
        if group_id != None: 
            _hdl = RBCategoryModel.objects.filter(group_id = group_id)
        else:
            _hdl = RBCategoryModel.objects.all()
        _rslt = []
        for _cat_obj in _hdl:
            _rslt.append({
                'category_id' : _cat_obj.id,
                'category_title' : _cat_obj.title,
                'group_id' : _cat_obj.group_id,
                'status' : _cat_obj.status
            })
        return _rslt
            
    @staticmethod
    def allgroups():
        _rslt = []
        for _group_obj in RBCategoryGroupModel.objects.all():
            _rslt.append({
                'group_id' : _group_obj.id,
                'title' : _group_obj.title,
                'status' : _group_obj.status,
                'category_count' : RBCategoryModel.objects.filter(group_id = _group_obj.id).count()
            })
        return _rslt

    @staticmethod
    def all_group_with_full_category():
        _rslt = RBCategory.allgroups()
        for _group in _rslt: 
            _group['content'] = []
            for _category_obj in RBCategoryModel.objects.filter(group_id = _group['group_id']):
                if _category_obj.image_store_hash:
                    _category_icon_large = settings.IMAGE_SERVER + _category_obj.image_store_hash + '_large' 
                    _category_icon_small = settings.IMAGE_SERVER + _category_obj.image_store_hash + '_small'
                else:
                    _category_icon_large = settings.IMAGE_SERVER + DEFAULT_CATEGORY_ICON_KEY + '_large' 
                    _category_icon_small = settings.IMAGE_SERVER + DEFAULT_CATEGORY_ICON_KEY + '_small'
                _group['content'].append({
                    'category_id' : _category_obj.id,
                    'category_title' : _category_obj.title,
                    'category_icon_large' : _category_icon_large,
                    'category_icon_small' : _category_icon_small
                })
        return _rslt
            
        
