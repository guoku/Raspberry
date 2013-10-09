# coding=utf8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5

class SessionKeyManager(models.Manager):
    def create_new_session(self, user_id, username, passwd, email):
        _session = username + passwd + email + unicode(datetime.now())
        _session_key = md5(_session.encode('utf-8')).hexdigest()
        _session_object = self.create(
            user_id = user_id, 
            session_key = _session_key
        )
        return _session_object

class Session_Key(models.Model):
    user = models.ForeignKey(User, related_name = "mobile_client_session")
    session_key = models.CharField(max_length = 64, unique = True, editable = False)
    create_time = models.DateTimeField(auto_now_add = True)
    objects = SessionKeyManager()
    
    def __unicode__(self):
        return self.session_key

class Device(models.Model):
    app_version = models.CharField(u'app版本', max_length = 25)
    dev_token = models.CharField(max_length = 64, db_index = True)
    dev_name = models.CharField(max_length = 255)
    dev_model = models.CharField(u'设备', max_length = 100)
    sys_version = models.CharField(u'设备版本', max_length = 25)
    push_badge = models.BooleanField(u'角标')
    push_alert = models.BooleanField(u'消息')
    push_sound = models.BooleanField(u'声音')
    development = models.BooleanField(u'沙箱')
    status = models.BooleanField(default = True)
    created_time = models.DateTimeField(auto_now_add = True, editable = False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    def __unicode__(self):
        return self.dev_name

    class Meta:
        ordering = ['-updated_time']

class User_Apns(models.Model):
    user = models.ForeignKey(User, related_name = "dev_token")
    device = models.ForeignKey(Device, unique = True)
    created_time = models.DateTimeField(auto_now_add = True, editable = False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ["-updated_time"]

