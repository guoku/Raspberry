# coding=utf-8
from celery.task import Task, PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
from utils.apns_notification import APNSWrapper

import base.selection as base_selection

import datetime
import time
import logging

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

logger = logging.getLogger('django.request')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)


scp_host = getattr(settings, 'SCP_HOST', '10.0.2.46')
scp_user = getattr(settings, 'SCP_USER', 'jiaxin')
scp_key = getattr(settings, 'SCP_KEY', '')
remote_file = getattr(settings, 'SCP_REMOTE_FILE', '/data/www/core/download/android/guoku-release.apk')

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

class PublishApkTask(Task):
    ignore_result = True
    time_limit = 1800
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY

    def run(self, filename):
        # client = scp.SCPClient(host=scp_host, user=scp_user, keyfile=scp_key)
        # pass
        # path_file =  filename

        ssh = SSHClient()
        # ssh.load_host_keys(filename=scp_key)
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=scp_host, username=scp_user, key_filename=scp_key)
        scp = SCPClient(ssh.get_transport())
        scp.put(filename, remote_file)
