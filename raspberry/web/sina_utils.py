from django.conf import settings
from base.cache import set_to_cache, get_from_cache, remove_from_cache
from weibo import APIClient

APP_KEY = getattr(settings, 'SINA_APP_KEY', None)
APP_SECRET = getattr(settings, 'SINA_APP_SECRET', None)
CALLBACK_URL = getattr(settings, 'SINA_BACK_URL', None)

def get_login_url(token):
    auth_client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL + "?token=" + token)
    return auth_client.get_authorize_url()

def get_sina_user_info(access_token, expires_in):
    auth_client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    auth_client.set_access_token(access_token = access_token, expires_in = expires_in)
    sina_id = auth_client.get.account__get_uid()['uid']
    return auth_client.get.users__show(access_token = access_token, uid = sina_id)

def get_sina_user_friends(sina_id, access_token, expires_in):
    auth_client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    auth_client.set_access_token(access_token = access_token, expires_in = expires_in)
    cursor = 0
    count = 200
    friends = []
    while True:
        result = auth_client.get.friendships__friends(access_token = access_token, uid = sina_id,
                                                      cursor = cursor, count = count)
        friends += result['users']
        if result['next_cursor'] != 0:
            cursor = result['next_cursor']
        else:
            break
    return friends

#def _gen_sina_user_info_cache_key(sina_id):
#    return "sina_user_info_cache_key_%s" % sina_id
#
#def set_sina_user_info_cache(sina_id, sina_user_info):
#    context = {}
#    context['screen_name'] = sina_user_info.name
#    context['avatar_small'] = sina_user_info.profile_image_url
#    context['avatar_large'] = sina_user_info.avatar_large
#    context['location'] = sina_user_info.location
#    context['gender'] = sina_user_info.gender
#    set_to_cache(_gen_sina_user_info_cache_key(sina_id), context)
#
#def get_sina_user_info_cache(sina_id):
#    return get_from_cache(_gen_sina_user_info_cache_key(sina_id))

def get_auth_data(code):
    auth_client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    auth_record = auth_client.request_access_token(code)
    sina_user = get_sina_user_info(auth_record.access_token, auth_record.expires_in)
    if not sina_user:
        return None
    sina_data = {}
    sina_data['access_token'] = auth_record.access_token
    sina_data['expires_in'] = auth_record.expires_in
    sina_data['sina_id'] = sina_user.id
    sina_data['screen_name'] = sina_user.name
    return sina_data
