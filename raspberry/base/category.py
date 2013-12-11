# coding=utf8
from models import Neo_Category_Group as CategoryGroupModel
from models import Neo_Category as CategoryModel
from models import Category as OldCategoryModel
from models import Taobao_Item_Neo_Category_Mapping as TaobaoItemNeoCategoryMappingModel 
from django.conf import settings
from django.db.models import Q
from hashlib import md5
from pymogile import Client
from wand.image import Image
import datetime 

class Old_Category(object):
    
    @staticmethod
    def find():
        _rslt = []
        for _obj in OldCategoryModel.objects.all():
            _rslt.append({
                'category_id' : _obj.id,
                'category_title' : _obj.title
            })
        return _rslt


class Category_Group(object):
    
    def __init__(self, category_group_id):
        self.category_group_id= int(category_group_id)
    
    def __ensure_category_group_obj(self):
        if not hasattr(self, 'category_group_obj'):
            self.category_group_obj = CategoryGroupModel.objects.get(pk = self.category_group_id)
    
    @classmethod
    def create(cls, title, status = 1):
        _category_group_obj = CategoryGroupModel.objects.create(
            title = title,
            status = status
        )
        return cls(_category_group_obj.id)
    
   
    def __load_category_group_context(self):
        self.__ensure_category_group_obj()
        _context = {}
        _context['category_group_id'] = self.category_group_obj.id
        _context['title'] = self.category_group_obj.title
        _context['status'] = self.category_group_obj.status
        return _context
   
    def read(self):
        return self.__load_category_group_context()
    
    def update(self, title = None, status = None):
        self.__ensure_category_group_obj()
        if title != None:
            self.category_group_obj.title = title
        if status != None:
            self.category_group_obj.status = status 
        self.category_group_obj.save() 



DEFAULT_CATEGORY_ICON_KEY = '03717fa531b23c6f5dbd5522e6eec9a1' 
class Category(object):
    
    def __init__(self, category_id):
        self.category_id= int(category_id)
    
    def __ensure_category_obj(self):
        if not hasattr(self, 'category_obj'):
            self.category_obj = CategoryModel.objects.get(pk = self.category_id)
    
    def __resize(self, data, w, h):
        _img = Image(blob = data)
        _img.resize(w, h)
        return _img.make_blob()
    
    def update(self, title = None, group_id = None, image_data = None, status = None):
        self.__ensure_category_obj()
        if title != None:
            self.category_obj.title = title
        if group_id != None:
            self.category_obj.group_id = group_id
        if status != None:
            self.category_obj.status = int(status)

        if image_data != None:
            self.__datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
            
            _key = md5(image_data).hexdigest()
            
            _large_data = self.__resize(image_data, 86, 86)
            _fp = self.__datastore.new_file('category/large/' + _key)
            _fp.write(_large_data)
            _fp.close()
            
            _small_data = self.__resize(image_data, 43, 43)
            _fp = self.__datastore.new_file('category/small/' + _key)
            _fp.write(_small_data)
            _fp.close()
            
            self.category_obj.image_store_hash = _key 
             
        self.category_obj.save()

    @classmethod
    def create(cls, title, group_id, status = 1):
        _category_obj = CategoryModel.objects.create(
            title = title,
            group_id = group_id,
            status = status
        )
        _inst = cls(_category_obj.id)
        _inst.category_obj = _category_obj
        return _inst
    
    def get_group_id(self):
        self.__ensure_category_obj()
        return self.category_obj.group_id
    
    def __load_category_context(self):
        self.__ensure_category_obj()
        _context = {}
        _context['category_id'] = self.category_obj.id
        _context['category_title'] = self.category_obj.title
        _context['group_id'] = self.category_obj.group_id
        _context['status'] = self.category_obj.status
        if self.category_obj.image_store_hash:
            _context['category_icon_large'] = settings.IMAGE_SERVER + 'category/large/' + self.category_obj.image_store_hash 
            _context['category_icon_small'] = settings.IMAGE_SERVER + 'category/small/' + self.category_obj.image_store_hash
        return _context

    
    def read(self):
        return self.__load_category_context()
    
    @staticmethod
    def get_category_title_dict():
        _dict = {}
        for _obj in CategoryModel.objects.all():
            _dict[_obj.id] = _obj.title
        return _dict
    
    @staticmethod
    def find(group_id = None, like_word = None, status = None, offset = None, count = None, order_by = None):
        _hdl = CategoryModel.objects.all()
        if group_id != None: 
            _hdl = _hdl.filter(group_id = group_id)
        if like_word != None: 
            _q = Q(title__icontains = like_word)
            _hdl = _hdl.filter(_q)

        if status == None:
            pass
        elif status > 0:
            _hdl = _hdl.filter(status__gt = 0)
        elif status == 0:
            _hdl = _hdl.filter(status__gte = 0)
        elif status < 0:
            _hdl = _hdl.filter(status__lt = 0)
            
        if order_by == '-status':
            _hdl = _hdl.order_by('-status')
        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]
        
        _rslt = []
        for _cat_obj in _hdl:
            _context = {
                'category_id' : _cat_obj.id,
                'category_title' : _cat_obj.title,
                'group_id' : _cat_obj.group_id,
                'status' : _cat_obj.status,
            }
            if _cat_obj.image_store_hash:
                _context['category_icon_large'] = settings.IMAGE_SERVER + 'category/large/' + _cat_obj.image_store_hash 
                _context['category_icon_small'] = settings.IMAGE_SERVER + 'category/small/' + _cat_obj.image_store_hash
            _rslt.append(_context)
        return _rslt
            
    @staticmethod
    def allgroups():
        _rslt = []
        for _group_obj in CategoryGroupModel.objects.all():
            _rslt.append({
                'group_id' : _group_obj.id,
                'title' : _group_obj.title,
                'status' : _group_obj.status,
                'category_count' : CategoryModel.objects.filter(group_id = _group_obj.id).count()
            })
        return _rslt

    @staticmethod
    def all_group_with_full_category():
        _rslt = Category.allgroups()
        for _group in _rslt: 
            _group['content'] = []
            for _category_obj in CategoryModel.objects.filter(group_id = _group['group_id'], status__gte = 0):
                _context = {
                    'category_id' : _category_obj.id,
                    'category_title' : _category_obj.title,
                    'status' : _category_obj.status
                }
                if _category_obj.image_store_hash:
                    _context['category_icon_large'] = settings.IMAGE_SERVER + 'category/large/' + _category_obj.image_store_hash
                    _context['category_icon_small'] = settings.IMAGE_SERVER + 'category/small/' + _category_obj.image_store_hash
                _group['content'].append(_context)
        return _rslt
            
        
    @staticmethod
    def get_category_by_taobao_cid(cid):
        _cid = int(cid)
        try:
            _obj = TaobaoItemNeoCategoryMappingModel.objects.get(taobao_category_id = _cid)
            return _obj.neo_category_id
        except TaobaoItemNeoCategoryMappingModel.DoesNotExist: 
            pass
        return 300 
