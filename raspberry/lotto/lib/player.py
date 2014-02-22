# coding=utf8
from lotto.models import Player
from mobile.models import Session_Key
from hashlib import md5
import datetime

def check_player(sina_id, screen_name, access_token, expires_in, mobile_session=None):
    try:
        _player = Player.objects.get(sina_id=sina_id)
        _player.access_token = access_token
        _player.expires_in = expires_in 
        _player.save()
    except Player.DoesNotExist:
        while True:
            _token = md5((screen_name + str(sina_id) + unicode(datetime.datetime.now())).encode('utf-8')).hexdigest()[0:16]
            try:
                Player.objects.get(token = _token)
            except:
                break
        _user_id = None
        try:
            if mobile_session != None:
                _user_id = Session_Key.objects.get_user_id(mobile_session)
        except:
            pass
        _player = Player.objects.create(
            sina_id = sina_id,
            user_id = _user_id,
            token = _token,
            screen_name = screen_name, 
            access_token = access_token,
            expires_in = expires_in
        )
    return _player.token

