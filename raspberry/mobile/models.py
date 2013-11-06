# coding=utf8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5

class SessionKeyManager(models.Manager):
    def generate_session(self, user_id, username, email, api_key):
        _session = username + email + api_key + unicode(datetime.now())
        _session_key = md5(_session.encode('utf-8')).hexdigest()
        _session_object = self.create(
            user_id = user_id,
            app_id = 1,
            session_key = _session_key
        )
        return _session_object
    
    def get_user_id(self, session_key):
        _session_object = self.get(
            session_key = session_key 
        )
        return _session_object.user_id

class AppsManager(models.Manager):
    def create_new_apps(self, user_id, **kwargs):
        _user = User.objects.get(pk = user_id)
        _app_name = kwargs.get('app_name', None)
        _app_desc = kwargs.get('app_desc', None)
        _api_key_string = _user.username + _user.email + datetime.now().strftime('%s')
        _api_key = md5(_api_key_string.encode('utf-8')).hexdigest()
        _api_secret_string = _user.username + _user.password + _api_key
        _api_secret = md5(_api_secret_string).hexdigest()
        _apps_obj = self.create(user=_user,
                                app_name=_app_name,
                                desc=_app_desc,
                                api_key=_api_key,
                                api_secret=_api_secret)
        return _apps_obj

class Apps(models.Model):
    user = models.ForeignKey(User)
    app_name = models.CharField(u'应用名称',max_length=30, unique=True)
    desc = models.TextField()
    api_key = models.CharField(max_length=64)
    api_secret = models.CharField(max_length=32)
    created_time = models.DateTimeField(auto_now=True)
    objects = AppsManager()
    class Meta:
        ordering = ['-created_time']

    def __unicode__(self):
        app_label = 'mobile'
        return self.app_name

class Session_Key(models.Model):
    user = models.ForeignKey(User, related_name = "mobile_client_session")
    app = models.ForeignKey(Apps)
    session_key = models.CharField(max_length = 64, unique = True, editable = False)
    create_time = models.DateTimeField(auto_now_add = True)
    objects = SessionKeyManager()
    
    def __unicode__(self):
        return self.session_key
    
    class Meta:
        app_label = 'mobile'

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
        app_label = 'mobile'
        ordering = ['-updated_time']

class User_Apns(models.Model):
    user = models.ForeignKey(User, related_name = "dev_token")
    device = models.ForeignKey(Device, unique = True)
    created_time = models.DateTimeField(auto_now_add = True, editable = False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        app_label = 'mobile'
        ordering = ["-updated_time"]

