# coding=utf8
from mobile.models import Device, User_Apns


class Apns(object):

    def __init__(self, dev_token):
        self.app_id = 1
        self.dev_token = dev_token 


    def create(self, **kwargs):
        _user_id = kwargs['user_id']
        _push_badge = True if kwargs['push_badge'] == "enabled" else False
        _push_alert = True if kwargs['push_alert'] == "enabled" else False
        _push_sound = True if kwargs['push_sound'] == "enabled" else False
        _development = True if kwargs['development'] == "sandbox" else False
        
        try:
            _device = Device.objects.get(
                dev_token = self.dev_token, 
                app = self.app_id
            )
            _device.app_id = self.app_id
            _device.dev_name = kwargs['dev_name']
            _device.dev_model = kwargs['dev_models']
            _device.app_version = kwargs['app_ver']
            _device.sys_version = kwargs['sys_ver']
            _device.push_badge = _push_badge
            _device.push_alert = _push_alert
            _device.push_sound = _push_sound
            _device.development = _development
            _device.save()
        except Device.DoesNotExist, e:
            _device = Device()
            _device.app_id = self.app_id
            _device.dev_token = self.dev_token
            _device.dev_name = kwargs['dev_name']
            _device.dev_model = kwargs['dev_models']
            _device.app_version = kwargs['app_ver']
            _device.sys_version = kwargs['sys_ver']
            _device.push_badge = _push_badge
            _device.push_alert = _push_alert
            _device.push_sound = _push_sound
            _device.development = _development
            _device.save()

        if _user_id:
            try:
                _user_apns = User_Apns.objects.get(device = _device.id)
                _user_apns.user_id = _user_id
                _user_apns.save()
            except User_Apns.DoesNotExist, e:
                _user_apns = User_Apns.objects.create(
                    device_id = _device.id, 
                    user_id = _user_id
                )

