# coding=utf-8
from celery.task import Task, PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
from django.template.loader import render_to_string
from models import Email_List 
from utils.mail import Mail
import datetime
import logging
import time

logger = logging.getLogger('django.request')
class GK3EDMTask(PeriodicTask):
    run_every = datetime.timedelta(seconds=3600) 
    ignore_result = True
    time_limit = 3500 
    queue = "edm"
    
    def run(self):
        _message = render_to_string('mail/gk3_announce.html')
        _mail = Mail(u"果库 3.0 隆重上线！", _message)
        count = 0
        for _obj in Email_List.objects.filter(done = False):
            try:
                _mail.send(
                    address = _obj.email 
                )
                _obj.done = True
                _obj.save()
                logger.info("[edm][info] %s sent success.", _obj.email)
            except Exception, e:
                logger.error("[edm][error] %s", e)
            count +=1
            if count >= 1000:
                break


