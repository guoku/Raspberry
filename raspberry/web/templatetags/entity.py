# coding=utf-8
from django.utils.log import getLogger
from django import template

import re

register = template.Library()
log = getLogger('django')

def display_note_item(note):
    return {
        'note_context' : note['note_context'],
        'creator_context' : note['creator_context'],
        'user_context' : note['user_context']
    }

register.inclusion_tag("entity/entity_note.html")(display_note_item)


def trans_category(value):
    log.info(value)

    return "分类"
register.filter('trans_category', trans_category)

def resize_image(value, size=640):
    # log.info(value)
    u = re.search("(alicdn|taobaocdn)\.com", value)
    log.info(u)
    if u:
        return "%s_%sx%s.jpg" % (value, size, size)
        # log.info(u.group())
    else:
        return value
        # log.info(u)
    # log.info(u.group())
    # return value

register.filter('resize', resize_image)