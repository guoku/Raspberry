# coding=utf-8
__author__ = 'edison'

from django.conf import settings
from django.utils.log import logger
from pyapns import configure, provision, notify

from mobile.models import User_Apns

PyAPNS_Server = getattr(settings, 'APNS_SERVER', None)
GUOKU_APNS_KEY = getattr(settings, 'GUOKU_APNS_KEY', None)

class APNSWrapper(object):
    guoku_apns_dir = GUOKU_APNS_KEY

    def __init__(self, user_id):
        # print "user user %s" % kwargs['user_id']
        # print kwargs
        configure(PyAPNS_Server)
        self.user_id = user_id
        # self.msg_type = kwargs['msg_type']
        self.notifications = {'aps':{
            'alert':None,
            'sound':'default',
            'badge':1,
            # 'message': {
                # 'user_id':self.user_id,
                # 'msg_type':msg_type,
            # },
        }}

    def badge(self, badge):
        self.notifications['aps']['badge'] = badge

    def alert(self, alert=None):
        self.notifications['aps']['alert'] = alert

    def message(self, message):
        self.notifications['aps']['message'] = message

    def push(self):
        user_apns = User_Apns.objects.filter(user=self.user_id)
        for apns in user_apns:
            logger.info("token %s" % apns.device.dev_token)

            if settings.DEBUG:
                if 'iPad' in apns.device.dev_name:
                    APNS_KEY = self.guoku_apns_dir + 'iPadCAPCK.sandbox.pem'
                    provision('com.guoku', open(APNS_KEY).read(), 'sandbox')
                else:
                    APNS_KEY = self.guoku_apns_dir + 'guokuCK.sandbox.pem'
                    provision('com.guoku.iphone', open(APNS_KEY).read(), 'sandbox')
            else:
                if 'iPad' in apns.device.dev_name:
                    APNS_KEY = self.guoku_apns_dir + 'iPadCAPCK.pem'
                    provision('com.guoku', open(APNS_KEY).read(), 'sandbox')
                else:
                    APNS_KEY = self.guoku_apns_dir + 'guokuCK.pem'
                    provision('com.guoku.iphone', open(APNS_KEY).read(), 'production')
            # logger.info(APNS_KEY)
            if 'iPad' in apns.device.dev_name:
                notify('com.guoku', apns.device.dev_token, self.notifications)
            else:
                notify('com.guoku.iphone', apns.device.dev_token, self.notifications)
