# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings

from lib.entity import MobileEntity
from lib.note import MobileNote

import datetime
import time

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class LikeEntityTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
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
