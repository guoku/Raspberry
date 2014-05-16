# coding=utf8
from models import Tag as TagModel
from models import Entity_Tag as EntityTagModel
from models import Recommend_User_Tag as RecommendUserTagModel 
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count 
from hashlib import md5

import datetime
import time
import urllib
import random 
import hmac
import hashlib

from django.utils.log import getLogger

log = getLogger('django')


class Tag(object):

    class Parser:
        
        @staticmethod
        def _is_in_tag_interval(ch):
            ch_unicode = ord(ch)
            if ch_unicode >= 19968 and ch_unicode <= 40895:
                return True
            if ch_unicode >= 12352 and ch_unicode <= 12447:
                return True
            if ch_unicode >= 12448 and ch_unicode <= 12543:
                return True
            if ch_unicode >= 97 and ch_unicode <= 122:
                return True
            if ch_unicode >= 65 and ch_unicode <= 90:
                return True
            if ch_unicode >= 48 and ch_unicode <= 57:
                return True
            return False
   
        @staticmethod
        def parse(text_string):
            tags = []
            
            text_string += " "
            i_sharp_start = None
            i = 0
            text_string_len = len(text_string)
            while i < text_string_len:
                if not Tag.Parser._is_in_tag_interval(text_string[i]):
                    if i_sharp_start != None:
                        if i > i_sharp_start:
                            tag = text_string[i_sharp_start:i]
                            if tags.count(tag) == 0:
                                tags.append(tag)
                        i_sharp_start = None
                if text_string[i] == "#" or text_string[i] == u"＃":
                    i_sharp_start = i + 1
                i += 1
            return tags
        
    @classmethod
    def cal_tag_hash(cls, tag_hash_string):
        _hash = None
        while True:
            _time_stamp = str(int(time.time()))
            _message = tag_hash_string.encode("utf8") + _time_stamp
            _hash = hmac.new("guokutag", _message, hashlib.md5).hexdigest()[0:8]
            try:
                TagModel.objects.get(tag_hash = _hash)
            except:
                break
        return _hash

    @classmethod
    def get_tag_hash_from_text(cls, tag_text):
        try:
            _tag = TagModel.objects.get(tag=tag_text)
            return _tag.tag_hash
        except TagModel.DoesNotExist, e:
            log.error("Error: %s" % e)
        return None

    @classmethod
    def get_tag_text_from_hash(cls, tag_hash):
        try:
            _tag = TagModel.objects.get(tag_hash=tag_hash)
            return _tag.tag
        except TagModel.DoesNotExist, e:
            log.error("Error: %s" % e)
        return None

    @classmethod
    def add_entity_tag(cls, entity_id, user_id, tag):
        try:
            _tag_obj = TagModel.objects.get(tag = tag)
        except TagModel.DoesNotExist, e:
            _tag_obj = TagModel.objects.create( 
                tag = tag,
                tag_hash = cls.cal_tag_hash(tag),
                creator_id = user_id,
                status = 0 
            )
        
        try:
            _entity_tag_obj = EntityTagModel.objects.get(entity = entity_id, user = user_id, tag = _tag_obj.id)
        except:
            _entity_tag_obj = EntityTagModel.objects.create(
                entity_id = entity_id,
                user_id = user_id,
                tag_id = _tag_obj.id,
                tag_text = _tag_obj.tag,
                tag_hash = _tag_obj.tag_hash,
                count = 0,
                last_tagged_time = datetime.datetime.now()
            )

        _entity_tag_obj.count += 1
        _entity_tag_obj.save()
        
        if RecommendUserTagModel.objects.filter(user = user_id, tag = tag):
            cls.update_recommend_user_tag_entity_count(user_id, tag)
       

    
    @classmethod
    def del_entity_tag(cls, entity_id, user_id, tag):
        try:
            _tag_obj = TagModel.objects.get(tag = tag)
            _entity_tag_obj = EntityTagModel.objects.get(entity = entity_id, user = user_id, tag = _tag_obj.id)
            if _entity_tag_obj.count > 1:
                _entity_tag_obj.count -= 1
                _entity_tag_obj.save()
            else:
                _entity_tag_obj.delete()
            
            if RecommendUserTagModel.objects.filter(user = user_id, tag = tag):
                cls.update_recommend_user_tag_entity_count(user_id, tag)
        except:
            pass
            
        

    @classmethod
    def entity_tag_stat(cls, entity_id):
        _entity_id = int(entity_id)
        # _tag_id_mapping = {}
        _entity_tags = []
        
        for _data in EntityTagModel.objects.filter(entity_id=_entity_id).values('tag_text', 'tag_id', 'tag_hash').annotate(user_count=Count('user')).order_by('-user_count'):
            log.info(_data)
            _entity_tags.append({
                'tag_id' : _data['tag_id'],
                'tag' : _data['tag_text'],
                'tag_hash' : _data['tag_hash'],
                'user_count' : _data['user_count'],
            })
        return _entity_tags
    
    
    @classmethod
    def user_tag_stat(cls, user_id):
        _user_id = int(user_id)
        _tag_id_mapping = {}
        _user_tags = []

        for _data in EntityTagModel.objects.filter(user_id=_user_id).values('tag_text', 'tag_id', 'tag_hash').annotate(entity_count=Count('entity')).order_by('-entity_count'):
            _user_tags.append({
                'tag_id' : _data['tag_id'],
                'tag' : _data['tag_text'],
                'tag_hash' : _data['tag_hash'],
                'entity_count' : _data['entity_count'],
            })

#        for _tag_obj in EntityTagModel.objects.filter(user_id = user_id):
#            _entity_id = _tag_obj.entity_id
#            if not _tag_obj.tag_id in _tag_id_mapping:
#                _tag = _tag_obj.tag.tag
#                _tag_id_mapping[_tag_obj.tag_id] = len(_user_tags)
#                _user_tags.append({
#                    'tag_id' : _tag_obj.tag_id,
#                    'tag' : _tag,
#                    'entity_id_list' : []
#                })
#            _user_tags[_tag_id_mapping[_tag_obj.tag_id]]['entity_id_list'].append(_entity_id)
        
        return _user_tags 
                
    @classmethod
    def get_user_tag_entity_count(cls, user_id, tag):
        return EntityTagModel.objects.filter(user = user_id, tag_text = tag).count()
        
    @classmethod
    def update_recommend_user_tag_entity_count(cls, user_id, tag): 
        try:
            _obj = RecommendUserTagModel.objects.get(user = user_id, tag = tag)
            _obj.entity_count = cls.get_user_tag_entity_count(user_id, tag)
            _obj.created_time = datetime.datetime.now() 
            _obj.save()
        except RecommendUserTagModel.DoesNotExist:
            pass
        
    @classmethod
    def add_recommend_user_tag(cls, user_id, tag):
        _entity_count = cls.get_user_tag_entity_count(user_id, tag)
        
        try:
            for _obj in EntityTagModel.objects.filter(user_id=user_id, tag_text=tag).order_by('-last_tagged_time'):
                _created_time = _obj.created_time
                break
        except Exception, e:
            _created_time = datetime.datetime.now()
        
        RecommendUserTagModel.objects.create(
            user_id=user_id,
            tag=tag,
            entity_count=_entity_count,
            created_time=_created_time
        )
    
    @classmethod
    def del_recommend_user_tag(cls, user_id, tag):
        try:
            _obj = RecommendUserTagModel.objects.get(
                user_id = user_id,
                tag = tag
            )
            _obj.delete()
        except RecommendUserTagModel.DoesNotExist:
            pass
    
    @classmethod
    def get_recommend_user_tag_list(cls, with_entity_count = True):
        _list = []
        _hdl = RecommendUserTagModel.objects.all()
        for _obj in _hdl: 
            tag_hash = Tag.get_tag_hash_from_text(_obj.tag)
            if with_entity_count:
                _list.append([_obj.user_id, _obj.tag , _obj.entity_count,tag_hash])
            else:
                _list.append([_obj.user_id, _obj.tag])
        return _list
                
    
    @classmethod
    def get_user_tag_entity_count(cls, user_id, tag):
        return EntityTagModel.objects.filter(user = user_id, tag_text = tag).count()
        
    @classmethod
    def search(cls, query_string):
        _query_set = TagModel.search.query(query_string)
        _tag_id_list = map(lambda x: int(x._sphinx['id']), _query_set)
        _tag_list = []
        for _tag_obj in TagModel.objects.filter(id__in=_tag_id_list):
            _tag_list.append({
                'tag' : _tag_obj.tag,
                'tag_id' : _tag_obj.id,
                'tag_hash' : _tag_obj.tag_hash
            })
        return _tag_list 
    
    @classmethod
    def find_tag_entity(cls, tag_hash):
        return map(lambda x: x, EntityTagModel.objects.filter(tag_hash=tag_hash, entity__weight__gt=0).order_by('-created_time').values_list('entity', flat=True).distinct())
        
    
    @classmethod
    def find_user_tag(cls, user_id = None, tag = None):
        _hdl = EntityTagModel.objects
        if user_id != None:
            _hdl = _hdl.filter(user_id = user_id) 
        if tag != None:
            _hdl = _hdl.filter(tag_text = tag) 
        return _hdl.values('user_id', 'tag_text').annotate(entity_count=Count('entity')).order_by('-entity_count')
    
    @classmethod
    def find_user_tag_entity(cls, user_id, tag):
        _user_id = int(user_id)
        _tag_id = TagModel.objects.get(tag = tag).id 
        _entity_id_list = map(lambda x: x.entity_id, EntityTagModel.objects.filter(user_id = _user_id, tag_id = _tag_id).order_by('-created_time'))
       
        return _entity_id_list
    
    
    @classmethod
    def __load_tag_prefix_index_from_cache(cls):
        _cache_key = 'tag_prefix_index'
        _index = cache.get(_cache_key)
        return _index
    
    @classmethod
    def __reset_tag_prefix_index_to_cache(cls):
        _cache_key = 'tag_prefix_index'
        _index = cache.get(_cache_key)
        _all_tags_sorted = map(lambda x: x.tag, TagModel.objects.all().order_by('tag')) 
        _index = {}
        for _tag in _all_tags_sorted:
            i = 0
            while i < len(_tag):
                _prefix = _tag[0 : i + 1]
                if not _index.has_key(_prefix):
                    _index[_prefix] = []
                _index[_prefix].append(_tag)
                i += 1
        cache.set(_cache_key, _index, 864000)
        return _index 

   
    @classmethod
    def read_tag_prefix_index(cls):
        _tag_prefix_index = cls.__load_tag_prefix_index_from_cache()
        if _tag_prefix_index == None:
            _tag_prefix_index = cls.__reset_tag_prefix_index_to_cache()
        return _tag_prefix_index 


    @classmethod
    def __load_user_latest_tag_list(cls, user_id):
        _cache_key = 'user_latest_tag_list_%s'%user_id 
        _list = cache.get(_cache_key)
        return _list
    
    @classmethod
    def __reset_user_latest_tag_list(cls, user_id):
        _cache_key = 'user_latest_tag_list_%s'%user_id
        _list = []
        for _tag_obj in EntityTagModel.objects.filter(user=user_id).order_by("-created_time")[0:10]:
            if not _tag_obj.tag_text in _list:
                _list.append(_tag_obj.tag_text)
        return _list
    
    
    @classmethod
    def read_user_latest_tag_list(cls, user_id):
        _user_latest_tag_list = cls.__load_user_latest_tag_list(user_id)
        if _user_latest_tag_list == None:
            _user_latest_tag_list = cls.__reset_user_latest_tag_list(user_id)
        return _user_latest_tag_list 
