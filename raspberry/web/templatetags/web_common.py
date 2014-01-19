# coding=utf-8

from django import template
import datetime
register = template.Library()


def format_time(value):
    time_interval = (datetime.datetime.now() - value).total_seconds()
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


def display_common_tag(tag_context):
    return {
        'tag_context' : tag_context
    }


register.inclusion_tag("common/tag.html")(display_common_tag)


def display_common_user(user_context):
    return {
        'user_context' : user_context,
    }


register.inclusion_tag("common/user.html")(display_common_user)