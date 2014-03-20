from django import template

from base.user import User
from django.utils.log import getLogger

register = template.Library()
log = getLogger('django')

def show_avater(value, size=64):
    _user_context = User(value).read()
    _avatar_url = _user_context['avatar_large']
    if size <= 50:
        _avatar_url = _user_context['avatar_small']

    return {
        'avatar_url' : _avatar_url,
        'nickname' : _user_context['nickname'],
        'size' : size,
    }

register.inclusion_tag("user/partial/avatar.html")(show_avater)
