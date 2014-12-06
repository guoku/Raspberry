# coding=utf-8
from django.utils.log import getLogger
from django import template
from base.category import Category
from base.category import Category_Group
from base.entity import Entity
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
    log.info(_category_context)
    _title = _category_context['category_title'].split('-')[0]
    return _title
register.filter('trans_category', trans_category)

def group_category(value):
    _category_context = Category(value).read()
    _category_group = Category_Group(_category_context['group_id']).read()
    log.info(_category_group)
    return _category_group['title']
register.filter('group_category', group_category)

def resize_image(value, size=640):
    if value is None:
        return None
    u = re.search("(alicdn|taobaocdn|taobao|guoku)\.com", value)
    if u:
        value = value.replace('_310x310.jpg', '')
        return "%s_%sx%s.jpg" % (value, size, size)
    else:
        return value
register.filter('resize', resize_image)

def entity_title(value):
    _entity_context = Entity(value).read()

    return _entity_context['title']
register.filter('entity_title', entity_title)

def entity_chief_image(value):
    _entity_context = Entity(value).read()

    return _entity_context['chief_image']['url']
register.filter('entity_chief_image', entity_chief_image)

def entity_hash(value):
    _entity_context = Entity(value).read()
    return _entity_context['entity_hash']
register.filter('entity_hash', entity_hash)