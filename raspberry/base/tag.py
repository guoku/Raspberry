# coding=utf8
from models import Tag as TagModel
from models import Entity_Tag as EntityTagModel
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
                count = 0,
                last_tagged_time = datetime.datetime.now()
            )
        
        _entity_tag_obj.count += 1
        _entity_tag_obj.save()
    
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
        except:
            pass
            
        

    @classmethod
    def user_tag_stat(cls, user_id):
        _user_id = int(user_id)
        _tag_id_mapping = {}
        _user_tags = []
        
        
        for _data in EntityTagModel.objects.filter(user_id = _user_id).values('tag').annotate(entity_count = Count('entity')).order_by('-entity_count'):
            _user_tags.append({
                'tag' : TagModel.objects.get(pk = _data['tag']).tag,
                'tag_id' : _data['tag'],
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
    def find_user_tag_entity(cls, user_id, tag):
        _user_id = int(user_id)
        _tag_id = TagModel.objects.get(tag = tag).id 
        _entity_id_list = map(lambda x: x.entity_id, EntityTagModel.objects.filter(user_id = _user_id, tag_id = _tag_id).order_by('-created_time'))
       
        return _entity_id_list
    
