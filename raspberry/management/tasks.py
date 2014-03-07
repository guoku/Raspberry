# coding=utf-8
from celery.task import Task, PeriodicTask 
from celery.task.schedules import crontab
from django.conf import settings
from utils.apns_notification import APNSWrapper

import base.selection as base_selection
from base.entity import Entity 
from base.note import Note 
from base.taobao_shop import TaobaoShop 
from utils.extractor.taobao import TaobaoExtractor 

import datetime
import time
import logging

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

logger = logging.getLogger('django')

MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)


scp_host = getattr(settings, 'SCP_HOST', '10.0.2.46')
scp_user = getattr(settings, 'SCP_USER', 'jiaxin')
scp_key = getattr(settings, 'SCP_KEY', None)
remote_file = getattr(settings, 'SCP_REMOTE_FILE', '/data/www/core/download/android/guoku-release.apk')

class PushMessageToUserTask(Task):
    ignore_result = True
    time_limit = 30
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
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
    time_limit = 600
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, select_count, start_time, interval_secs = 600):
        _t_start = datetime.datetime.now()
        base_selection.arrange_entity_note_selection( 
            select_count = select_count,
            start_time = start_time, 
            interval_secs = interval_secs 
        )
        print "selection arranged...%s secs cost" % str(datetime.datetime.now() - _t_start)

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

class MergeEntityTask(Task):
    ignore_result = True
    time_limit = 30
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, entity_id, target_entity_id):
        _entity = Entity(entity_id)
        _entity.merge(target_entity_id)

class FreezeUserEntityNoteAll(Task):
    ignore_result = True
    time_limit = 30
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id):
        _user_id = int(user_id)
        for _note_id in Note.find(user_id=_user_id, status=1):
            try:
                _note = Note(_note_id)
                _entity_id = _note.get_entity_id()
                _entity = Entity(_entity_id)
                _entity.update_note(
                    note_id = _note_id,
                    weight = -1 
                )
            except Exception, e:
                pass
            logger.info("entity note [%d] of [%d] freezed..."%(_note_id, _user_id))


class PublishApkTask(Task):
    ignore_result = True
    time_limit = 1800
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"

    def run(self, filename):
        # client = scp.SCPClient(host=scp_host, user=scp_user, keyfile=scp_key)
        # pass
        # path_file =  filename
        key_filename = scp_key + 'id_rsa'
        ssh = SSHClient()
        # ssh.load_host_keys(filename=scp_key)
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname = scp_host, username = scp_user, key_filename = key_filename)
        scp = SCPClient(ssh.get_transport())
        scp.put(filename, remote_file)
