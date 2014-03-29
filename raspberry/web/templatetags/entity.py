# coding=utf-8
from django.utils.log import getLogger
from django import template
from base.category import Category

import re

register = template.Library()
log = getLogger('django')

def display_note_item(note, is_staff=False):
    return {
        'note_context' : note['note_context'],
        'creator_context' : note['creator_context'],
        'user_context' : note['user_context'],
        'poke_button_target_status' : note['poke_button_target_status'],
        'is_staff' : is_staff,
    }

register.inclusion_tag("entity/entity_note.html")(display_note_item)

def trans_category(value):
    _category_context = Category(value).read()
    _title = _category_context['category_title'].split('-')[0]
    return _title
register.filter('trans_category', trans_category)

def resize_image(value, size=640):
    u = re.search("(alicdn|taobaocdn|taobao)\.com", value)
    if u:
        value = value.replace('_310x310.jpg', '')
        return "%s_%sx%s.jpg" % (value, size, size)
    else:
        return value
register.filter('resize', resize_image)
