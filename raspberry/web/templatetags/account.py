# coding=utf-8
from django import template
register = template.Library()


def display_avatar_update(user_context):
    return {
        'user_context' : user_context
    }

register.inclusion_tag("account/partial/display_avatar_update.html")(display_avatar_update)