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


def display_like_entity(entity_context, already_like):
    return {
        'entity_id' : entity_context['entity_id'],
        'like_count' : entity_context['like_count'],
        'already_like' : already_like
    }

register.inclusion_tag("common/like_entity.html")(display_like_entity)