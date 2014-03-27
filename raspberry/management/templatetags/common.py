# coding=utf-8

import datetime
import HTMLParser
from django import template
register = template.Library()

def format_time(value):
    time_interval = (datetime.datetime.now() - value).total_seconds()
    if time_interval < 60:
        return "%d 秒前"%(time_interval)
    elif time_interval < 60 * 60:
        return "%d 分钟前"%((time_interval / 60) + 1)
    elif time_interval < 60 * 60 * 24: 
        return "%d 小时前"%(time_interval / (60 * 60) + 1)
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    return "%d 年 %d 月 %d 日"%(value.year, value.month, value.day)  
register.filter(format_time)

def add(a, b):
    return a + b
register.filter(add)

def minus(a, b):
    return a - b
register.filter(minus)

def mod(a, b):
    return a % b
register.filter(mod)

def count(value):
    if value == None:
        return 0
    return len(value)
register.filter(count)

def top(array, count):
    return array[::-1][0 : 0 + count] 
register.filter(top)

def date_format(value):
    if value == None:
        return 'None'
    return "%d-%d-%d %d:%d:%d"%(value.year, value.month, value.day, value.hour, value.minute, value.second)  
register.filter(date_format)

def html_unescape(text):
    return HTMLParser.HTMLParser().unescape(text) 
register.filter(html_unescape)

