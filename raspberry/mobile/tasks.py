# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings

from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser

import datetime
import time
import logging
logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class LikeEntityTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    queue = "default"
    
    def run(self, entity_id, request_user_id = None):
        _entity_id = int(entity_id)
        _request_user_id = int(request_user_id)
        MobileEntity(_entity_id).like(_request_user_id)

class UnlikeEntityTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, entity_id, request_user_id = None):
        _entity_id = int(entity_id)
        _request_user_id = int(request_user_id)
        MobileEntity(_entity_id).unlike(_request_user_id)

class FollowUserTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, follower_id, followee_id):
        MobileUser(follower_id).follow(followee_id)

class UnfollowUserTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, follower_id, followee_id):
        MobileUser(follower_id).unfollow(followee_id)

class PokeEntityNoteTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, note_id, request_user_id = None):
        _note_id = int(note_id)
        _request_user_id = int(request_user_id)
        MobileNote(note_id).poke(_request_user_id)

class DepokeEntityNoteTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, note_id, request_user_id = None):
        _note_id = int(note_id)
        _request_user_id = int(request_user_id)
        MobileNote(note_id).depoke(_request_user_id)

class DeleteEntityNoteTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, entity_id, note_id):
        _entity = MobileEntity(entity_id)
        _entity.del_note(note_id)

class DeleteEntityNoteCommentTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, note_id, comment_id):
        _note = MobileNote(note_id)
        _note.del_comment(comment_id)

class RetrievePasswordTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, user_id):
        _user = MobileUser(user_id)
        _user.retrieve_password() 

class MarkFootprint(Task):
    ignore_result = True
    time_limit = 5 
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, user_id, message = False, selection = False, social_feed = False, friend_feed = False):
        MobileUser(user_id).mark_footprint(
            message = message,
            selection = selection,
            social_feed = social_feed,
            friend_feed = friend_feed
        )
