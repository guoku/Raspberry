from django import template

from base.user import User
from django.utils.log import getLogger

register = template.Library()
log = getLogger('django')

def show_avater(value, size=64):
    _user_context = User(value).read()
    # log.info(_user_context)
    _avatar_url = _user_context['avatar_large']
    if size <= 50:
        _avatar_url = _user_context['avatar_small']

    return {
        'avatar_url' : _avatar_url,
        'nickname' : _user_context['nickname'],
        'size' : size,
    }

register.inclusion_tag("user/partial/avatar.html")(show_avater)


def show_auth_user(user_id):
    _user_context = User(user_id).read()
    log.info(_user_context)
    return {
        'user_context':_user_context,
    }
register.inclusion_tag("user/partial/auth.html")(show_auth_user)