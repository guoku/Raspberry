# coding=utf-8
from celery.task import Task, PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
from utils.apns_notification import APNSWrapper

import base.selection as base_selection

import datetime
import time
import logging
logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class PushMessageToUserTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, user_id, badge, message, testor_id): 
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = badge) 
        _apns.alert(message)
        _apns.message(message = {
            'testor' : testor_id, 
            'type' : 'broadcast' 
        })
        _apns.push()

class ArrangeSelectionTask(Task):
    ignore_result = True
    time_limit = 1800
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, select_count, start_time, interval_secs = 600):
        _t_start = datetime.datetime.now()
        base_selection.arrange_entity_note_selection( 
            select_count = select_count,
            start_time = start_time, 
            interval_secs = interval_secs 
        )
        print "selection arranged...%s secs cost" % str(datetime.datetime.now() - _t_start)
    

