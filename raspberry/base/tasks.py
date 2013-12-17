# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings

from message import EntityNoteMessage
#import popularity
#import selection 
import datetime
import time

POPULAR_ENTITY_RUN_INTERVAL_SECS = getattr(settings, 'POPULAR_ENTITY_RUN_INTERVAL_SECS', 600)
MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

#class CalPopularEntity(PeriodicTask):
#    ignore_result = True
#    time_limit = 600
#    run_every = datetime.timedelta(seconds = POPULAR_ENTITY_RUN_INTERVAL_SECS) 
#    
#    def run(self):
#        t_start = datetime.datetime.now()
#        popularity.generate_popular_entity()
#        print "popular entity updated...%s secs cost" % str(datetime.datetime.now() - t_start)
#
#class ArrangeSelection(PeriodicTask):
#    ignore_result = True
#    time_limit = 1800
#    run_every = crontab(minute = 0, hour = 12) #run at 2:30 am every day
#    
#    def run(self):
#        _t_start = datetime.datetime.now() + datetime.timedelta(days = 1) 
#        _year = _t_start.year
#        _month = _t_start.month
#        _date = _t_start.day
#        selection.arrange( 
#            select_count = 91,
#            start_time = datetime.datetime(_year, _month, _date, 8, 0, 0),
#            interval_secs = 600 
#        )
#        print "selection arranged...%s secs cost" % str(datetime.datetime.now() - _t_start)
    
class CreateEntityNoteMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    
    def run(self, user_id, user_unread_message_count, entity_id, note_id): 
        _message = EntityNoteMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count, 
            entity_id = entity_id,
            note_id = note_id
        )

