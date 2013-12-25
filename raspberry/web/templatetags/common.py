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