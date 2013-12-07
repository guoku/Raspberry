# coding=utf8
from models import Tag as TagModel
from models import Entity_Tag as EntityTagModel
from django.conf import settings
from django.core.cache import cache

import datetime
import urllib
import random 
import time



class Tag(object):
    

    @classmethod
    def user_tags(cls, user_id): 
        
        for _tag_obj in EntityTagModel.objects.filter(creator_id = user_id):
        
        
                'key' : _obj.key,
                'content_type' : _obj.content_type,
                'weight' : _obj.weight
            })

        return _banner_context_list
    
