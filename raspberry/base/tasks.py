# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings

import popularity
import datetime
import time

POPULAR_ENTITY_RUN_INTERVAL_SECS = getattr(settings, 'POPULAR_ENTITY_RUN_INTERVAL_SECS', 600)
class CalPopularEntity(PeriodicTask):
    ignore_result = True
    time_limit = 600
    run_every = datetime.timedelta(seconds = POPULAR_ENTITY_RUN_INTERVAL_SECS) 
    
    def run(self):
        t_start = datetime.datetime.now()
        popularity.generate_popular_entity()
        print "popular entity updated...%s secs cost" % str(datetime.datetime.now() - t_start)

