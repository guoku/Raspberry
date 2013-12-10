# coding=utf8
from models import Tag as TagModel
from models import Entity_Tag as EntityTagModel
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count 

import datetime
import urllib
import random 
import time



class Tag(object):
    

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
    
