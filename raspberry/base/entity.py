# coding=utf8
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Sum
from mongoengine import *
from utils.apns_notification import APNSWrapper
import datetime
import urllib
import random 
import time


from category import Category 
from image import Image
from item import Item
from models import Entity as EntityModel
from models import Entity_Like as EntityLikeModel
from models import Taobao_Item_Category_Mapping as TaobaoItemCategoryMappingModel
from models import Note as NoteModel
from models import NoteSelection
from tasks import CreateEntityNoteMessageTask, CreateNoteSelectionMessageTask
from note import Note
from user import User 
from hashlib import md5




class Entity(object):
    
    class Mark(object):
        promoted = 1
        first = 2
        event = 3
        media = 4
        celebrity = 5
        award = 6

        @staticmethod
        def all():
            return [
                { 'value' : 0, 'title' : 'none' },
                { 'value' : 1, 'title' : 'promoted' },
                { 'value' : 2, 'title' : 'first' },
                { 'value' : 3, 'title' : 'event' },
                { 'value' : 4, 'title' : 'media' },
                { 'value' : 5, 'title' : 'celebrity' },
                { 'value' : 6, 'title' : 'award' }
            ]
        
        @staticmethod
        def get_title(value):
            if value == 1:
                return 'promoted'
            elif value == 2:
                return 'first'
            elif value == 3:
                return 'event'
            elif value == 4:
                return 'media'
            elif value == 5:
                return 'celebrity'
            elif value == 6:
                return 'award'
            return 'none' 


    def __init__(self, entity_id):
        self.entity_id = int(entity_id)
    
    def __ensure_entity_obj(self):
        if not hasattr(self, 'entity_obj'):
            self.entity_obj = EntityModel.objects.get(pk = self.entity_id)

    @classmethod
    def cal_entity_hash(cls, entity_hash_string):
        while True:
            _hash = md5((entity_hash_string + unicode(datetime.datetime.now())).encode('utf-8')).hexdigest()[0:8]
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
            
        
        _entity_hash = cls.cal_entity_hash(taobao_item_info['taobao_id'] + taobao_item_info['title'] + taobao_item_info['shop_nick'])
        
        try:
            _obj = TaobaoItemCategoryMappingModel.objects.get(taobao_category_id = taobao_item_info["cid"])
            _old_category_id = _obj.guoku_category_id
        except:
            _old_category_id = 12
            
        _entity_obj = EntityModel.objects.create( 
            entity_hash = _entity_hash,
            creator_id = creator_id,
            category_id = _old_category_id,
            neo_category_id = category_id,
            brand = brand,
            title = title,
            intro = intro,
            price = taobao_item_info["price"], 
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
        
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
    
    
    
    def del_image(self, image_id):
        self.__ensure_entity_obj()
        if image_id in self.entity_obj.detail_images:
            self.entity_obj.detail_images = self.entity_obj.detail_images.replace(image_id, '')
            self.entity_obj.detail_images = self.entity_obj.detail_images.replace('##', '#')
            if len(self.entity_obj.detail_images) > 1 and self.entity_obj.detail_images[0] == '#':
                self.entity_obj.detail_images = self.entity_obj.detail_images[1:]
            if len(self.entity_obj.detail_images) > 1 and self.entity_obj.detail_images[-1] == '#':
                self.entity_obj.detail_images = self.entity_obj.detail_images[:-1]
        self.entity_obj.save()
    
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
    
    
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

    @classmethod
    def get_entity_id_by_hash(cls, entity_hash):
        _cache_key = 'entity_%s_hash_to_id'%entity_hash
        _entity_id = cache.get(_cache_key)
        if _entity_id == None:
            try:
                _entity_id = EntityModel.objects.get(entity_hash = entity_hash).id
                cache.set(_cache_key, _entity_id, 8640000)
            except EntityModel.DoesNotExist, e:
                pass
        return _entity_id 
    

    def __load_basic_info_from_cache(self):
        _cache_key = 'entity_%s_basic_info'%self.entity_id
        _basic_info = cache.get(_cache_key)
        return _basic_info
        
    def __reset_basic_info_to_cache(self, basic_info = None):
        _cache_key = 'entity_%s_basic_info'%self.entity_id
        if basic_info == None:
            self.__ensure_entity_obj()
            _basic_info = {}
            _basic_info['entity_id'] = self.entity_obj.id
            _basic_info['brand'] = self.entity_obj.brand 
            _basic_info['title'] = self.entity_obj.title
            _basic_info['intro'] = self.entity_obj.intro
            _basic_info['price'] = self.entity_obj.price
            _basic_info['creator_id'] = self.entity_obj.creator_id
            _basic_info["entity_hash"] = self.entity_obj.entity_hash
            _basic_info["old_category_id"] = self.entity_obj.category_id
            _basic_info["category_id"] = self.entity_obj.neo_category_id
            _basic_info['like_count'] = self.entity_obj.like_count 
            _basic_info["created_time"] = self.entity_obj.created_time
            _basic_info["updated_time"] = self.entity_obj.updated_time
            _basic_info["weight"] = self.entity_obj.weight
            _basic_info["mark_value"] = self.entity_obj.mark
            _basic_info["mark"] = Entity.Mark.get_title(self.entity_obj.mark)
            
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
        else:
            _basic_info = basic_info
        cache.set(_cache_key, _basic_info, 864000)
        ## CLEAN_OLD_CACHE ## 
        cache.delete("entity_context_%s"%self.entity_id)
        
        return _basic_info
        

    def __load_note_info_from_cache(self):
        _cache_key = 'entity_%s_note_info'%self.entity_id
        _note_info = cache.get(_cache_key)
        return _note_info
    
    def __reset_note_info_to_cache(self, note_info = None):
        _cache_key = 'entity_%s_note_info'%self.entity_id
        if note_info == None:
            _note_id_list = Note.find(entity_id = self.entity_id, status = 1)
            _note_info = {
                'total_score' : 0, 
                'score_count' : 0, 
                'note_id_list' : _note_id_list,
                'note_count' : len(_note_id_list)
            }
        else:
            _note_info = note_info
        cache.set(_cache_key, _note_info, 864000)
        
        ## CLEAN_OLD_CACHE ## 
        cache.delete("entity_note_context_list_%s"%self.entity_id)

        return _note_info
        
    def __read_basic_info(self):
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info == None:
            _basic_info = self.__reset_basic_info_to_cache()
        return _basic_info 
    
    def __read_item_info(self):
        _item_info = { 'item_id_list' : Item.find(entity_id = self.entity_id) } 
        return _item_info
    
    def __read_note_info(self):
        _note_info = self.__load_note_info_from_cache()
        if _note_info == None:
            _note_info = self.__reset_note_info_to_cache()
        return _note_info
    
    def read(self, json = False):
        _context = self.__read_basic_info()
        if json:
            _context['price'] = unicode(_context['price'])
            _context['created_time'] = time.mktime(_context['created_time'].timetuple())
            _context['updated_time'] = time.mktime(_context['updated_time'].timetuple())
        _context.update(self.__read_item_info())
        _context.update(self.__read_note_info())

        return _context    
    
    
    def delete(self):
        self.__ensure_entity_obj()
        self.entity_obj.delete()

        # TODO: removing entity_id in item
    
    def update(self, category_id = None, old_category_id = None, brand = None, title = None, intro = None, price = None, chief_image_id = None, weight = None, mark = None):
        
        self.__ensure_entity_obj()
        if brand != None:
            self.entity_obj.brand = brand
        if title != None:
            self.entity_obj.title = title
        if intro != None:
            self.entity_obj.intro = intro
        if price != None:
            self.entity_obj.price = price
        if category_id != None:
            self.entity_obj.neo_category_id = int(category_id)
        if old_category_id != None:
            self.entity_obj.category_id = int(old_category_id) 
        if weight != None:
            self.entity_obj.weight = int(weight)
        if mark != None:
            self.entity_obj.mark = int(mark)
        
        if chief_image_id != None and chief_image_id != self.entity_obj.chief_image:
            _detail_image_ids = self.entity_obj.detail_images.split('#')
            if chief_image_id in _detail_image_ids:
                _detail_image_ids.remove(chief_image_id)
            if self.entity_obj.chief_image not in _detail_image_ids:
                _detail_image_ids.insert(0, self.entity_obj.chief_image)
            self.entity_obj.detail_images =  "#".join(_detail_image_ids)
            self.entity_obj.chief_image = chief_image_id
            
        self.entity_obj.save()
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
            
    @classmethod
    def find(cls, root_old_category_id = None, category_id = None, like_word = None, timestamp = None, status = None, offset = None, count = 30, sort_by = None, reverse = False):
        _hdl = EntityModel.objects.all()
        if root_old_category_id != None and root_old_category_id >= 1 and root_old_category_id <= 11:
            _hdl = _hdl.filter(category__pid = root_old_category_id)
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        if like_word != None: 
            _q = Q(title__icontains = like_word)
            _hdl = _hdl.filter(_q)
        if status == -1:
            _hdl = _hdl.filter(weight = -1)
        elif status == -2:
            _hdl = _hdl.filter(weight = -2)
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
        elif sort_by == 'note':
            if reverse:
                _hdl = _hdl.annotate(note_count = Count('note')).order_by('note_count')
            else:
                _hdl = _hdl.annotate(note_count = Count('note')).order_by('-note_count')
        elif sort_by == 'time':
            if reverse:
                _hdl = _hdl.order_by('created_time')
            else:
                _hdl = _hdl.order_by('-created_time')
        else:
            _hdl = _hdl.order_by('-weight', '-like_count')
             
        
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
    def _load_entity_pool(cls, category_id):
        if category_id == None:
            _cache_key = 'entity_pool_all'
        else:
            _cache_key = 'entity_pool_%s'%category_id
        _pool = cache.get(_cache_key)
        return _pool
    
    @classmethod
    def _reset_entity_pool(cls, category_id):
        if category_id == None:
            _cache_key = 'entity_pool_all'
        else:
            _cache_key = 'entity_pool_%s'%category_id
        
        _hdl = EntityModel.objects.filter(weight__gte = 0)
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        _pool = map(lambda x: x.id, _hdl)
        
        cache.set(_cache_key, _pool, 86400)
        return _pool
    
    
    @classmethod
    def roll(cls, category_id = None, count = 10):
        _pool = cls._load_entity_pool(category_id)
        if _pool == None:
            _pool = cls._reset_entity_pool(category_id)
        
        if len(_pool) <= count:
            return _pool 
        return random.sample(_pool, count) 

        
    @classmethod
    def count(cls, category_id = None, status = None):
        _hdl = EntityModel.objects.all()
        if category_id != None:
            _hdl = _hdl.filter(neo_category_id = category_id)
        if status != None:
            if status == -1:
                _hdl = _hdl.filter(weight = -1)
            elif status == -2:
                _hdl = _hdl.filter(weight = -2)
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
        
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info['like_count'] = _like_count
            self.__reset_basic_info_to_cache(_basic_info)



    def like(self, user_id):
        try:
            _user_id = int(user_id)
            EntityLikeModel.objects.create(
                entity_id = self.entity_id,
                user_id = _user_id
            )
            self.update_like_count()
            User(_user_id).update_user_like_count(delta = 1)
            cache.delete("gk_e_like_u2elt_%s"%user_id)

#########################   REMOVE LIKE MESSAGE AT FIRST ##########################
#            _basic_info = self.__read_basic_info()
#            if _basic_info.has_key('creator_id') and _basic_info['creator_id'] != None and _basic_info['creator_id'] != user_id:
#                if EntityLikeMessage.objects.filter(user_id = _basic_info['creator_id'], entity_id = self.entity_id, liker_id = _user_id).count() == 0: 
#                    _message = EntityLikeMessage(
#                        user_id = _basic_info['creator_id'],
#                        entity_id = self.entity_id,
#                        liker_id = _user_id, 
#                        created_time = datetime.datetime.now()
#                    )
#                    _message.save()

            return True
        except:
            pass
        return False
         
    def unlike(self, user_id):
        try:
            _user_id = int(user_id)
            _obj = EntityLikeModel.objects.get(
                entity_id = self.entity_id,
                user_id = _user_id
            )
            _obj.delete()
            User(_user_id).update_user_like_count(delta = -1)
            cache.delete("gk_e_like_u2elt_%s"%user_id)
            
#            _basic_info = self.__read_basic_info()
#            if _basic_info.has_key('creator_id') and _basic_info['creator_id'] != None:
#                for _doc in EntityLikeMessage.objects.filter(user_id = _basic_info['creator_id'], entity_id = self.entity_id, liker_id = _user_id):
#                    _doc.delete()
            
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
        
        _list = []
        for _obj in _hdl[offset : offset + count]:
            _list.append([_obj.entity_id, _obj.created_time])

        return _list
        
    def add_note(self, creator_id, note_text, score = 0, image_data = None):
        _note = Note.create(
            entity_id = self.entity_id,
            creator_id = creator_id,
            note_text = note_text,
            score = score,
            image_data = image_data
        )

        _note_info = self.__load_note_info_from_cache()
        if _note_info != None:
            _note_info['note_count'] += 1
            _note_info['note_id_list'].append(_note.note_id) 
            self.__reset_note_info_to_cache(_note_info)

        _creator = User(creator_id)
        _creator.update_user_entity_note_count(delta = 1)
                
        _basic_info = self.__read_basic_info()
        if _basic_info.has_key('creator_id') and _basic_info['creator_id'] != None and _basic_info['creator_id'] != int(creator_id):
            CreateEntityNoteMessageTask.delay(
                user_id = _basic_info['creator_id'],
                user_unread_message_count = User(_basic_info['creator_id']).get_unread_message_count(),
                entity_id = self.entity_id,
                note_id = _note.note_id, 
            )
        
        return _note
    
    def del_note(self, note_id):
        _note_id = int(note_id)
        _note = Note(note_id)
        _note_context = _note.read()
        _note.delete()  
        
        _note_info = self.__load_note_info_from_cache()
        if _note_info != None:
            if _note.note_id in _note_info['note_id_list']:
                _note_info['note_count'] -= 1
                _note_info['note_id_list'].remove(_note.note_id)
            self.__reset_note_info_to_cache(_note_info)
        
        User(_note_context['creator_id']).update_user_entity_note_count(delta = -1)
        for _doc in EntityNoteMessage.objects.filter(entity_id = self.entity_id, note_id = _note_id):
            _doc.delete()
    
    def update_note_selection_info(self, note_id, selector_id, selected_time, post_time):
        _note_id = int(note_id)
        if selector_id != None:
            _selector_id = int(selector_id)
        else:
            _selector_id = None 
        
        _note = Note(note_id)
        _note.update_selection_info(
            selector_id = _selector_id,
            selected_time = selected_time,
            post_time = post_time
        )
        
        ## CLEAN_OLD_CACHE ## 
        cache.delete("entity_key_note_id_%s"%self.entity_id)
        cache.delete("entity_note_context_list_%s"%self.entity_id)
        cache.delete("note_context_%s"%note_id)
        
        if _selector_id == None:
            for _doc in NoteSelection.objects.filter(note_id = _note_id):
                _doc.delete()
        else: 
            _doc = NoteSelection.objects.filter(note_id = _note_id).first()
            if _doc == None:
                self.__ensure_entity_obj()
                _doc = NoteSelection(
                    selector_id = _selector_id,
                    selected_time = selected_time,
                    post_time = post_time,
                    entity_id = self.entity_id, 
                    note_id = _note_id,
                    root_category_id = self.entity_obj.category.pid,
                    category_id = self.entity_obj.category_id,
                    neo_category_group_id = Category(self.entity_obj.neo_category_id).get_group_id(), 
                    neo_category_id = self.entity_obj.neo_category_id, 
                )
                _doc.save()
                
                if self.entity_obj.weight < 0:
                    self.update(weight = 0)
               
                _note_context = _note.read()
                CreateNoteSelectionMessageTask.delay(
                    user_id = _note_context['creator_id'], 
                    user_unread_message_count = User(_note_context['creator_id']).get_unread_message_count(),
                    entity_id = self.entity_id,
                    note_id = _note_id, 
                )
            
            
            else:
                _doc.selector_id = _selector_id 
                _doc.selected_time = selected_time
                _doc.post_time = post_time
            _doc.save()


    def update_note(self, note_id, score = None, note_text = None, image_data = None, weight = None):
        _note = Note(note_id)
        _note.update(
            score = score,
            note_text = note_text,
            image_data = image_data,
            weight = weight
        )

        if weight != None:
            if int(weight) < 0:
                self.update_note_selection_info(
                    note_id = note_id,
                    selector_id = None,
                    selected_time = None, 
                    post_time = None
                )
            self.__reset_note_info_to_cache()
        
    
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
    
    @staticmethod
    def read_entity_note_figure_data_by_store_key(store_key): 
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        return _datastore.get_file_data(store_key)


    @staticmethod
    def _available_for_selection(selected, cand):
        i = len(selected) - 1
        while (i > len(selected) - 3) and (i >= 0):
            if cand['root_category_id'] == selected[i]['root_category_id']:
                return False
            i -= 1
        return True
    
    @staticmethod
    def arrange_entity_note_selection(select_count, start_time, interval_secs):
        _freezing_time = datetime.datetime(2099, 1, 1) 
        
        _selection_cands = []
        for _doc in NoteSelection.objects.filter(post_time__gt = _freezing_time).order_by("selected_time"):
            _selection_cands.append({
                'entity_id' : _doc.entity_id,
                'note_id' : _doc.note_id,
                'selector_id' : _doc.selector_id,
                'selected_time' : _doc.selected_time,
                'root_category_id' : _doc.root_category_id
            })
        
        _selected = []
        f = True
        while f:
            i = 0
            f = False
            while i < len(_selection_cands): 
                if Entity._available_for_selection(_selected, _selection_cands[i]):
                    _selection = _selection_cands.pop(i)
                    _selected.append(_selection)
                    
                    f = True
                    if len(_selected) >= select_count:
                        f = False
                        break
                else:
                    i += 1
       
        _post_time = start_time
        for _selection in _selected:
            Entity(_selection['entity_id']).update_note_selection_info(
                note_id = _selection['note_id'],
                selector_id = _selection['selector_id'],
                selected_time = _selection['selected_time'],
                post_time = _post_time
            )
            print "[%s:%s] [%d] arranged @ [%s]"%(_selection['entity_id'], _selection['note_id'], _selection['root_category_id'], _post_time)
            _post_time += datetime.timedelta(seconds = interval_secs)
        print "%d selection arranged in total"%len(_selected)
    
    
