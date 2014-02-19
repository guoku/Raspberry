from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from base.user import User
import random
import string
def signup(email, password, nickname, **kwargs):
    _new_user = User.create(email = email, password = password)
    _new_user.set_profile(nickname = nickname,
                          location = kwargs.get("location"),
                          city = kwargs.get("city"),
                          gender = kwargs.get("gender"),
                          bio = kwargs.get("bio"),
                          website = kwargs.get("website"))
    return _new_user

def get_login_redirect_url(request):
    next_url = get_redirect_url(request)
    if next_url:
        return next_url
    return reverse("web_selection")

def get_redirect_url(request):
    next_url = request.REQUEST.get("next", None)
    if not next_url:
        next_url = request.META.get('HTTP_REFERER', None)
    return next_url

def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None

def get_random_string(length):
    s = ""
    for i in range(length):
        s += random.choice(string.letters + string.digits)
    return s

def generate_random_storage_key(prefix):
    return prefix + "_" + get_random_string(10)
    
def create_temporary_storage(key, **kwargs):
    cache.set(key, kwargs, 3600)

def get_temporary_storage(key):
    return cache.get(key)

def delete_temporary_storage(key):
    cache.delete(key)

def update_temporary_storage(key, **kwargs):
    data = get_temporary_storage(key)
    data.update(kwargs)
    cache.set(key, data)

