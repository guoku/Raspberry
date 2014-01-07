from django.conf import settings
import urllib
import urllib2

TAOBAO_TOKEN_URL = 'https://oauth.taobao.com/token'

class TaobaoClient():

    def __init__(self, code, app_key, app_secret, redirect_uri):
        self.app_key = app_key
        self.code = code
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri

    def get_post_data(self):
        param = {}
        param['grant_type'] = 'authorization_code'
        param['code'] = self.code
        param['client_id'] = self.app_key
        param['client_secret'] = self.app_secret
        param['redirect_uri'] = self.redirect_uri
        param['view'] = 'web'
        return param

    def get_res(self):
        param = urllib.urlencode(self.get_post_data())
        token_url = TAOBAO_TOKEN_URL
        res = urllib2.urlopen(token_url, param)
        data = res.read()
        return data

