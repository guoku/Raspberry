# coding=utf-8
from django import template
from base.user import User
from django.utils.log import getLogger
register = template.Library()

log = getLogger('django')

def display_avatar_update(user_context):
    return {
        'user_context' : user_context
    }

register.inclusion_tag("account/partial/avatar_update.html")(display_avatar_update)

def show_auth_user(user_id):
    _user_context = User(user_id).read()
    return {
        'user_context':_user_context,
    }
register.inclusion_tag("account/partial/auth.html")(show_auth_user)
