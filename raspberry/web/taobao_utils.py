from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import simplejson as json
from urllib import urlencode
from web.platforms.user_status import *
from taobaoapi.user import TaobaoUser
from taobaoapi.utils import *
from base.cache import set_to_cache, get_from_cache, remove_from_cache
import base.user as base_user
import taobao as taobao_client
import time

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

def _get_taobao_user_info(access_token):
    return TaobaoUser(APP_KEY, APP_SECRET).get_user(access_token)

def _gen_taobao_user_info_cache_key(taobao_id):
    return "taobao_user_info_cache_key_%s" % taobao_id

def set_taobao_user_info_cache(taobao_id, taobao_user_info):
    context = {}
    context['screen_name'] = taobao_user_info['nick']
    context['avatar_large'] = taobao_user_info['avatar']
    set_to_cache(_gen_taobao_user_info_cache_key(taobao_id), context)

def get_taobao_user_info_cache(taobao_id):
    return get_from_cache(_gen_taobao_user_info_cache_key(taobao_id))

def auth(request):
    code = request.GET.get('code', None)
    redirect_url = get_referer_url(request, request.session['back_to_url'])
    auth_client = taobao_client.TaobaoClient(code = code,
                                          app_key = APP_KEY,
                                          app_secret = APP_SECRET,
                                          redirect_uri = redirect_url)
    auth_record = json.loads(auth_client.get_res())
    request.session['taobao_access_token'] = auth_record['access_token']
    request.session['taobao_refresh_token'] = auth_record['refresh_token']
    request.session['taobao_id'] = auth_record['taobao_user_id']
    request.session['taobao_expires_in'] = auth_record['expires_in']
    request.session['taobao_re_expires_in'] = auth_record['re_expires_in']
    return redirect_url

def get_login_url():
    return _get_oauth_url(OAUTH_URL, CALLBACK_URL)      

def create_token_if_not_existed(request):
    access_token = request.session['taobao_access_token']
    refresh_token = request.session['taobao_refresh_token']
    taobao_id = request.session['taobao_id']
    expires_in = request.session['taobao_expires_in']
    re_expires_in = request.session['taobao_re_expires_in']

    taobao_user = _get_taobao_user_info(access_token)
    user_id = request.user.id
    if taobao_user:
        taobao_token = base_user.read_taobao_token_by_user_id(user_id)
        if taobao_token:
            if unicode(taobao_token['taobao_id']) != unicode(taobao_id):
                token = base_user.read_taobao_token(taobao_id)
                if token:
                    return -2
                return -1
        else:
            taobao_token = base_user.read_taobao_token(taobao_id)
            if not taobao_token:
                taobao_token = base_user.create_taobao_token(user_id = user_id, taobao_id = taobao_id,
                                                            access_token = access_token,
                                                            refresh_token = refresh_token,
                                                            screen_name = taobao_user['nick'],
                                                            expires_in = expires_in,
                                                            re_expires_in = re_expires_in)
                return 1
            else:
                return -2
        if taobao_token['expires_in'] < time.time():
            base_user.update_taobao_token(taobao_id = taobao_id,
                                          access_token = access_token,
                                          refresh_token = refresh_token,
                                          screen_name = taobao_user['nick'],
                                          expires_in = expires_in,
                                          re_expires_in = re_expires_in)
            return 2
    return 0


def check_user_status(request):
    access_token = request.session['taobao_access_token']
    refresh_token = request.session['taobao_refresh_token']
    taobao_id = request.session['taobao_id']
    taobao_user = _get_taobao_user_info(access_token)
    print taobao_user
    request.session['taobao_screen_name'] = taobao_user['nick']
    set_taobao_user_info_cache(taobao_id, taobao_user)
    if taobao_user:
        user = None
        taobao_token = base_user.read_taobao_token(taobao_id)
        if taobao_token:
            user = base_user.read_user_context(taobao_token['user_id'])
            if taobao_token['expires_in'] < time.time():
                base_user.update_taobao_token(taobao_id = taobao_id,
                                              access_token = access_token,
                                              refresh_token = refresh_token,
                                              screen_name = taobao_user['nick'],
                                              expires_in = request.session['taobao_expires_in'],
                                              re_expires_in = request.session['taobao_re_expires_in'] )

            if base_user.check_if_set_password(user['user_id']) and \
                base_user.check_if_set_email(user['user_id']):
                return CAN_LOGIN, user
            else:
                return NEED_TO_SET_EMAIL_OR_PASSWORD, user
        else:
            return NEED_TO_REGISTER, None
    else:
        return NO_THIRD_PARTY_USER, None

