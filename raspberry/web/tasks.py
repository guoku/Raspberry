# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
import datetime
import time
import logging
import lib.logger as web_logger 
logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class WebLogTask(Task):
    ignore_result = True
    time_limit = 10 
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "log"
    
    def run(self, duration, page, request, ip, log_time, entry='web', request_user_id=None, appendix=None):
        _prev_str = request.get('prev', None)
        
        web_logger.log(
            duration=duration,
            ip=ip,
            log_time=log_time,
            page=page,
            request_user_id=request_user_id,
            prev_str=_prev_str,
            appendix=appendix,
        )

