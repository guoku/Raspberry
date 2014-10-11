# from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from base.user import User
from utils.lib import get_random_string
import re
# import random
# import string

log = getLogger('django')


def signup(email, password, nickname, **kwargs):
    _new_user = User.create(email=email, password=password)
    _new_user.set_profile(
        nickname=nickname,
        location=kwargs.get("location"),
        city=kwargs.get("city"),
        gender=kwargs.get("gender"),
        bio=kwargs.get("bio"),
        website=kwargs.get("website")
    )
    return _new_user

def get_login_redirect_url(request):
    pattern = re.compile(r'like|follow|comment|poke')
    next_url = get_redirect_url(request)

    match = pattern.search(next_url)

    if match:
        return request.META['HTTP_REFERER']

    if next_url:
        return next_url
    return reverse("web_selection")

def get_redirect_url(request):
    next_url = request.REQUEST.get("next", None)
    return next_url

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

