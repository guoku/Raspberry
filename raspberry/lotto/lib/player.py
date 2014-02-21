# coding=utf8
from lotto.models import Player

def check_player(sina_id, screen_name, access_token, expires_in):
    try:
        _player = Player.objects.get(sina_id=sina_id)
    except Player.DoesNotExist:
        _player = Player.objects.create(
            sina_id = sina_id,
            token = 'abc',
            screen_name = screen_name, 
            access_token = access_token,
            expires_in = expires_in
        )
    return _player.token

                



