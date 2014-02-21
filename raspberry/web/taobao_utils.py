from django.conf import settings
from django.utils import simplejson as json
import urllib
import urllib2

from urllib import urlencode
from utils.taobaoapi.user import TaobaoUser
from utils.taobaoapi.utils import *
import time

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

def get_referer_url(request, back_url = None):
    host = request.META['HTTP_HOST']
    if not back_url:
        referer_url = request.META.get('HTTP_REFERER', None)
    else:
        referer_url = "http://" + host + back_url
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url

def _get_oauth_url(action, back_url):
    param = {'client_id' : APP_KEY, 'response_type' : 'code',
             'redirect_uri' : back_url, 'view' : 'web'}
    return "%s?%s" % (action, urlencode(param))

def get_taobao_user_info(access_token):
    return TaobaoUser(APP_KEY, APP_SECRET).get_user(access_token)

def auth(request):
    code = request.GET.get('code', None)
    redirect_url = get_referer_url(request, request.session.get('back_to_url', None))
    auth_client = TaobaoClient(code = code,
                               app_key = APP_KEY,
                               app_secret = APP_SECRET,
                               redirect_uri = redirect_url)
    auth_record = json.loads(auth_client.get_res())
    request.session['taobao_access_token'] = auth_record['access_token']
    request.session['taobao_id'] = auth_record['taobao_user_id']
    request.session['taobao_expires_in'] = auth_record['expires_in']
    return redirect_url

def get_login_url():
    return _get_oauth_url(OAUTH_URL, CALLBACK_URL)      

