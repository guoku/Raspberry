# coding=utf8
from models import Entity as EntityModel
from models import Entity_Like as EntityLikeModel
from models import Note as NoteModel
from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum
from mongoengine import *
from note import Note
from item import Item
from image import Image
from hashlib import md5
import datetime
import urllib
import random 
import time



class Entity(object):

    def __init__(self, entity_id):
        self.entity_id = int(entity_id)
    
    def __ensure_entity_obj(self):
        if not hasattr(self, 'entity_obj'):
            self.entity_obj = EntityModel.objects.get(pk = self.entity_id)

    
    @classmethod
    def cal_entity_hash(cls, entity_hash_string):
        while True:
            _hash = md5(entity_hash_string + unicode(datetime.datetime.now())).hexdigest()[0:8]
            try:
                Entity.objects.get(entity_hash = _hash)
            except:
                break
        return _hash 
    
    def __insert_taobao_item(self, taobao_item_info, images):
        _taobao_item = Item.create_taobao_item( 
            entity_id = self.entity_id,
            images = images,
            taobao_id = taobao_item_info["taobao_id"],
            cid = taobao_item_info["cid"],
            title = taobao_item_info["title"],
            shop_nick = taobao_item_info["shop_nick"], 
            price = taobao_item_info["price"], 
            soldout = taobao_item_info["soldout"], 
        )
        return _taobao_item.item_id
    
    @classmethod
    def create_by_taobao_item(cls, creator_id, category_id, chief_image_url, 
                              taobao_item_info, brand = "", title = "", intro = "", detail_image_urls = [], 
                              weight = 0):
        
        _chief_image_id = Image.get_image_id_by_origin_url(chief_image_url)
        if _chief_image_id == None:
            _chief_image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], chief_image_url)
            _chief_image_id = _chief_image_obj.image_id
        
        _detail_image_ids = []
        for _image_url in detail_image_urls:
            _image_id = Image.get_image_id_by_origin_url(_image_url)
            if _image_id == None:
                _image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], _image_url)
                _image_id = _image_obj.image_id
            _detail_image_ids.append(_image_id)
            
        
        _entity_hash = cls.cal_entity_hash(taobao_item_info['taobao_id'])
        _entity_obj = EntityModel.objects.create( 
            entity_hash = _entity_hash,
            creator_id = creator_id,
            neo_category_id = category_id,
            brand = brand,
            title = title,
            intro = intro,
            chief_image = _chief_image_id,
            detail_images = "#".join(_detail_image_ids),
            weight = weight
        )
         
        _item_images = _detail_image_ids
        _item_images.append(_chief_image_id)
        
        _inst = cls(_entity_obj.id)
        _inst.entity_obj = _entity_obj
        _taobao_item_id = _inst.__insert_taobao_item(taobao_item_info, _item_images)

        return _inst

    
    def merge(self, target_entity_id):
        _item_id_list = Item.get_item_id_list_by_entity_id(target_entity_id)
        for _item_id in _item_id_list:
            _item = Item(_item_id)
            _item.bind(self.entity_id)
        
        _target_entity = Entity(target_entity_id)
        _target_entity.delete()
    
    def add_image(self, image_url = None, image_data = None):
        _image_obj = Image.create(
            source = 'gk_management', 
            origin_url = image_url,
            image_data = image_data
        )
        self.__ensure_entity_obj()
        if not _image_obj.image_id in self.entity_obj.detail_images:
            if len(self.entity_obj.detail_images) > 0:
                self.entity_obj.detail_images += '#'
            self.entity_obj.detail_images += _image_obj.image_id
        self.entity_obj.save() 
    
    
    
    def del_image(self, image_id):
        self.__ensure_entity_obj()
        if image_id in self.entity_obj.detail_images:
            self.entity_obj.detail_images = self.entity_obj.detail_images.replace(image_id, '')
            self.entity_obj.detail_images = self.entity_obj.detail_images.replace('##', '#')
            if self.entity_obj.detail_images[0] == '#':
                self.entity_obj.detail_images = self.entity_obj.detail_images[1:]
            if self.entity_obj.detail_images[-1] == '#':
                self.entity_obj.detail_images = self.entity_obj.detail_images[:-1]
        self.entity_obj.save()
    
    
    
    def add_taobao_item(self, taobao_item_info, image_urls = []):
        _image_ids = []
        for _image_url in image_urls:
            _image_obj = Image.create('tb_' + taobao_item_info['taobao_id'], _image_url)
            _image_ids.append(_image_obj.image_id)
        
        _item_id = self.__insert_taobao_item( 
            taobao_item_info = taobao_item_info,
            images = _image_ids
        )
        
        self.__ensure_entity_obj()
        if taobao_item_info['price'] < self.entity_obj.price:
            self.entity_obj.price = taobao_item_info['price']
            self.entity_obj.save()
        return _item_id 


    
    def __load_entity_basic_info(self, json = False):
        self.__ensure_entity_obj()
        _basic_info = {}
        _basic_info['entity_id'] = self.entity_obj.id
        _basic_info['brand'] = self.entity_obj.brand 
        _basic_info['title'] = self.entity_obj.title
        _basic_info['intro'] = self.entity_obj.intro
        
        if json:
            _basic_info['price'] = unicode(self.entity_obj.price)
        else: 
            _basic_info['price'] = self.entity_obj.price
        _basic_info["entity_hash"] = self.entity_obj.entity_hash
        _basic_info["category_id"] = self.entity_obj.neo_category_id
        _basic_info['like_count'] = self.entity_obj.like_count 
        if json:
            _basic_info['created_time'] = time.mktime(self.entity_obj.created_time.timetuple())
        else:
            _basic_info["created_time"] = self.entity_obj.created_time
        if json:
            _basic_info['updated_time'] = time.mktime(self.entity_obj.updated_time.timetuple())
        else:
            _basic_info["updated_time"] = self.entity_obj.updated_time
        _basic_info["weight"] = self.entity_obj.weight
        
        _basic_info['chief_image'] = {
            'id' : self.entity_obj.chief_image,
            'url' : Image(self.entity_obj.chief_image).getlink(),
        }
        _basic_info['detail_images'] = []
        for _image_id in self.entity_obj.detail_images.split('#'):
            if len(_image_id) > 0:
                _basic_info['detail_images'].append({
                    'id' : _image_id,
                    'url' : Image(_image_id).getlink()
                })
        return _basic_info
        
        
    
    def __load_item_info(self):
        _item_info = { 'item_id_list' : Item.find(entity_id = self.entity_id) } 
        return _item_info

    def __load_note_info(self):
        _cache_key = 'entity_%s_note_info'%self.entity_id
        _note_info = cache.get(_cache_key)
        print _note_info
        if _note_info == None:
            _note_info = {
                'total_score' : 0, 
                'score_count' : 0, 
                'note_count' : 0, 
                'note_id_list' : [],
            }
            for _note_obj in NoteModel.objects.filter(entity_id = self.entity_id):
                _note_info['note_id_list'].append(_note_obj.id)
                if _note_obj.score != 0:
                    _note_info['total_score'] += _note_obj.score
                    _note_info['score_count'] += 1
                _note_info['note_count'] += 1
            cache.set(_cache_key, _note_info, 864000)

        return _note_info
        
    def __update_note_info(self, note_info):
        _cache_key = 'entity_%s_note_info'%self.entity_id
        cache.set(_cache_key, note_info, 864000)

    def read(self, json = False):
        _context = self.__load_entity_basic_info(json)
        _context.update(self.__load_item_info())
        _context.update(self.__load_note_info())

        return _context    
    
    
    def delete(self):
        self.__ensure_entity_obj()
        self.entity_obj.delete()

        # TODO: removing entity_id in item
    
    def update(self, category_id = None, brand = None, title = None, intro = None, price = None, chief_image_id = None, weight = None):
        self.__ensure_entity_obj()
        if category_id != None:
            self.entity_obj.neo_category_id = category_id 
        if brand != None:
            self.entity_obj.brand = brand
        if title != None:
            self.entity_obj.title = title
        if intro != None:
            self.entity_obj.intro = intro
        if price != None:
            self.entity_obj.price = price
        if category_id != None:
            self.entity_obj.category_id = int(category_id)
        if weight != None:
            self.entity_obj.weight = int(weight)
        
        if chief_image_id != None and chief_image_id != self.entity_obj.chief_image:
            _detail_image_ids = self.entity_obj.detail_images.split('#')
            if chief_image_id in _detail_image_ids:
                _detail_image_ids.remove(chief_image_id)
            if self.entity_obj.chief_image not in _detail_image_ids:
                _detail_image_ids.insert(0, self.entity_obj.chief_image)
            self.entity_obj.detail_images =  "#".join(_detail_image_ids)
            self.entity_obj.chief_image = chief_image_id
            
        self.entity_obj.save()
            
    @classmethod
    def find(cls, category_id = None, like_word = None, timestamp = None, status = None, offset = None, count = 30, sort_by = None, reverse = False):
        _hdl = EntityModel.objects.all()
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        if like_word != None: 
            _q = Q(title__icontains = like_word)
            _hdl = _hdl.filter(_q)
        if status < 0:
            _hdl = _hdl.filter(weight__lt = 0)
        elif status >= 0:
            _hdl = _hdl.filter(weight__gte = 0)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        
        if sort_by == 'price':
            if reverse:
                _hdl = _hdl.order_by('-price')
            else:
                _hdl = _hdl.order_by('price')
        elif sort_by == 'like':
            if reverse:
                _hdl = _hdl.order_by('like_count')
            else:
                _hdl = _hdl.order_by('-like_count')
        else:
            _hdl = _hdl.order_by('-created_time')
        
        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]
        
        _entity_id_list = map(lambda x: x.id, _hdl)
        return _entity_id_list
    
    @classmethod
    def search(cls, query_string, offset = 0, count = 30):
        _query_set = EntityModel.search.query(query_string).filter(like_count__gte = 0)
        _entity_id_list = []
        for _result in _query_set[offset : offset + count]:
            _entity_id_list.append(int(_result._sphinx["id"]))
        return _entity_id_list 

    @classmethod
    def roll(cls, category_id = None, count = 10):
        _hdl = EntityModel.objects.filter(weight__gte = 0)
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        _entity_id_list = map(lambda x: x.id, _hdl)
        if len(_entity_id_list) <= count:
            return _entity_id_list
        return random.sample(_entity_id_list, count) 

        
    @classmethod
    def count(cls, category_id = None, status = None):
        _hdl = EntityModel.objects.all()
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        if status != None:
            if status < 0:
                _hdl = _hdl.filter(weight__lt = 0)
            elif status >= 0:
                _hdl = _hdl.filter(weight__gte = 0)
        return _hdl.count()
    
    def bind_item(self, item_id):
        _item_obj = Item(item_id)
        _item_obj.bind_entity(self.entity_id)
    
    def unbind_item(self, item_id):
        _item_obj = Item(item_id)
        if _item_obj.get_entity_id() == self.entity_id:
            _item_obj.bind(-1)

    def update_like_count(self):
        self.__ensure_entity_obj()
        _like_count = EntityLikeModel.objects.filter(entity_id = self.entity_id).count()
        self.entity_obj.like_count = _like_count
        self.entity_obj.save()


    def like(self, user_id):
        try:
            EntityLikeModel.objects.create(
                entity_id = self.entity_id,
                user_id = user_id
            )
            self.update_like_count()

            return True
        except:
            pass
        return False
         
    def unlike(self, user_id):
        try:
            _obj = EntityLikeModel.objects.get(
                entity_id = self.entity_id,
                user_id = user_id
            )
            _obj.delete()
            return True
        except:
            pass
        return False
         
    def like_already(self, user_id):
        return EntityLikeModel.objects.filter(user_id = user_id, entity_id = self.entity_id).count() > 0 

    @staticmethod
    def like_list_of_user(user_id, timestamp = None, offset = 0, count = 30):
        _user_id = int(user_id)
        _hdl = EntityLikeModel.objects.filter(user_id = _user_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        return map(lambda x : x.entity_id, _hdl[offset : offset + count])
        
    def add_note(self, creator_id, note_text, score = 0, image_data = None):
        _note = Note.create(
            entity_id = self.entity_id,
            creator_id = creator_id,
            note_text = note_text,
            score = score,
            image_data = image_data
        )

        _note_info = self.__load_note_info()
        if _note_info != None:
            _note_info['note_count'] += 1
            _note_info['note_id_list'].append(_note.note_id) 
            if score != 0:
                _note_info['total_score'] += score
                _note_info['score_count'] += 1
            self.__update_note_info(_note_info)
        
        return _note
    
#    def update_note(self, note_id, score, note_text, image_data = None):
#        _note_id = int(note_id)
#        _score = int(score)
#        _note = Note(_note_id)
#        _note.update(
#            note_text = note_text,
#            image_data = image_data
#        )
#        return _note
        
    
#    @staticmethod
#    def get_user_entity_note_count(user_id):
#        _user_id = int(user_id)
#        return EntityNoteModel.objects.filter(creator_id = _user_id).count()
    
    @staticmethod
    def get_user_like_count(user_id):
        _user_id = int(user_id)
        return EntityLikeModel.objects.filter(user_id = _user_id).count()
    
    
    @staticmethod
    def get_user_last_like(user_id):
        _user_id = int(user_id)
        try:
            _obj = EntityLikeModel.objects.filter(user_id = _user_id).order_by('-created_time')[0]
            return _obj.entity_id
        except:
            pass
        return None
    
#    @staticmethod
#    def find_entity_note(entity_id = None, creator_id_set = None, timestamp = None, offset = None, count = None):
#        _hdl = EntityNoteModel.objects.all()
#        if entity_id != None:
#            _hdl = _hdl.filter(entity_id = entity_id)
#        if creator_id_set != None:
#            _hdl = _hdl.filter(creator_id__in = creator_id_set)
#        if timestamp != None:
#            _hdl = _hdl.filter(created_time__lt = timestamp)
#        
#        if offset != None and count != None:
#            _hdl = _hdl[offset : offset + count]
#        _rslt = []
#        for _obj in _hdl:
#            _rslt.append({
#                'entity_id' : _obj.entity_id,
#                'note_id' : _obj.note_id,
#                'score' : _obj.score,
#                'creator_id' : _obj.creator_id
#            })
#        return _rslt 
#        
#    
    
    @staticmethod
    def read_entity_note_figure_data_by_store_key(store_key): 
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        return _datastore.get_file_data(store_key)
