# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings

from base.entity import Entity
from base.note import Note
from base.user import User
from base.taobao_shop import TaobaoShop 
from utils.extractor.taobao import TaobaoExtractor 

import datetime
import time
import logging
logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class LikeEntityTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, entity_id, request_user_id = None):
        _entity_id = int(entity_id)
        _request_user_id = int(request_user_id)
        Entity(_entity_id).like(_request_user_id)

class UnlikeEntityTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, entity_id, request_user_id = None):
        _entity_id = int(entity_id)
        _request_user_id = int(request_user_id)
        Entity(_entity_id).unlike(_request_user_id)

class FollowUserTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, follower_id, followee_id):
        User(follower_id).follow(followee_id)

class UnfollowUserTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, follower_id, followee_id):
        User(follower_id).unfollow(followee_id)

class PokeEntityNoteTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, note_id, request_user_id = None):
        _note_id = int(note_id)
        _request_user_id = int(request_user_id)
        Note(note_id).poke(_request_user_id)

class DepokeEntityNoteTask(Task):
    ignore_result = True
    time_limit = 10
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, note_id, request_user_id = None):
        _note_id = int(note_id)
        _request_user_id = int(request_user_id)
        Note(note_id).depoke(_request_user_id)

class DeleteEntityNoteTask(Task):
    ignore_result = True
    time_limit = 20
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, entity_id, note_id):
        _entity = Entity(entity_id)
        _entity.del_note(note_id)

class DeleteEntityNoteCommentTask(Task):
    ignore_result = True
    time_limit = 20
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, note_id, comment_id):
        _note = Note(note_id)
        _note.del_comment(comment_id)

class RetrievePasswordTask(Task):
    ignore_result = True
    time_limit = 30
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id):
        _user = User(user_id)
        _user.retrieve_password() 

class MarkFootprint(Task):
    ignore_result = True
    time_limit = 10 
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, message = False, selection = False, social_feed = False, friend_feed = False):
        User(user_id).mark_footprint(
            message = message,
            selection = selection,
            social_feed = social_feed,
            friend_feed = friend_feed
        )

class CreateTaobaoShopTask(Task):
    ignore_result = True
    time_limit = 30
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, nick, shop_link):
        if not TaobaoShop.nick_exist(nick):
            _shop_info = TaobaoExtractor.fetch_shop(shop_link)
            _shop = TaobaoShop.create(
                nick = nick,
                shop_id = _shop_info['shop_id'],
                title = _shop_info['title'],
                shop_type  = _shop_info['type'],
                seller_id = _shop_info['seller_id'],
                pic_path = _shop_info['pic']
            )