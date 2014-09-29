# coding=utf-8

from django import template
# from django.conf import settings
from django.utils.log import getLogger
from datetime import datetime
import time

from base.entity import Entity

register = template.Library()

log = getLogger('django')


def format_time(value):

    before_time = time.mktime(value.timetuple())
    now = time.mktime(datetime.now().timetuple())
    time_interval = now - before_time

    if time_interval < 60:
        return "%d 秒前" % (time_interval)
    elif time_interval < 60 * 60:
        return "%d 分钟前" % ((time_interval / 60) + 1)
    elif time_interval < 60 * 60 * 24:
        return "%d 小时前" % (time_interval / (60 * 60) + 1)
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    return "%d 年 %d 月 %d 日" % (value.year, value.month, value.day)

register.filter(format_time)

def selection_previous_paginator(value):
    if value % 3 == 0:
        value -= 2
    return value
register.filter(selection_previous_paginator)

def selection_next_paginator(value):
    if value % 3 == 2:
        value += 2

    return value
register.filter(selection_next_paginator)

def display_web_paginator(paginator):
    return {
        "paginator" : paginator
    }

register.inclusion_tag("common/web_paginator.html")(display_web_paginator)


def display_common_entity(entity_context):
    return {
        'entity_context' : entity_context
    }


register.inclusion_tag("common/entity.html")(display_common_entity)


def display_common_note(note):
    return {
        'note' : note
    }
register.inclusion_tag("common/note.html")(display_common_note)


def display_common_tag(tag_context, user_id=None):
    return {
        'tag_context' : tag_context,
        'user_id' : user_id
    }
register.inclusion_tag("common/tag.html")(display_common_tag)


def display_common_user(user_context):
    user_context['latest_like_entities'] = []
    if user_context.has_key('latest_like_entity_id_list'):
        for _e_id in user_context['latest_like_entity_id_list'][0:6]:
            try:
                user_context['latest_like_entities'].append(Entity(_e_id).read())
            except Exception, e:
                pass
    return {
        'user_context' : user_context,
    }
register.inclusion_tag("common/user.html")(display_common_user)
