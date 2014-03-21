# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
import datetime
import time
import logging
import lib.logger as mobile_logger 
logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class MobileLogTask(Task):
    ignore_result = True
    time_limit = 10 
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "log"
    
    def run(self, duration, view, request, ip, log_time, entry='mobile', request_user_id=None, appendix=None):
        _version = request.get('version', 'unkown')
        _device = request.get('device', None)
        _duid = request.get('duid', None)
        _os = request.get('os', None)
        _channel = request.get('channel', None)
        _prev_str = request.get('prev', None)
        
        mobile_logger.log(
            entry=entry,
            duration=duration,
            ip=ip,
            log_time=log_time,
            view=view,
            request_user_id=request_user_id,
            version=_version,
            device=_device,
            duid=_duid,
            os=_os,
            channel=_channel,
            prev_str=_prev_str,
            appendix=appendix,
        )

