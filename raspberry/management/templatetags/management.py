# coding=utf-8
from django import template
from django.conf import settings
register = template.Library()


def display_entity_row(entity_context):
    return {
        "entity_context" : entity_context,
    } 
register.inclusion_tag("entity/partial/row.html")(display_entity_row)

DEFAULT_CATEGORY_ICON_KEY = '03717fa531b23c6f5dbd5522e6eec9a1' 
def display_category_row(category_context):
    if not category_context.has_key('category_icon_large'):
        category_context['category_icon_large'] = settings.IMAGE_SERVER + 'category/large/' + DEFAULT_CATEGORY_ICON_KEY
        category_context['category_icon_small'] = settings.IMAGE_SERVER + 'category/small/' + DEFAULT_CATEGORY_ICON_KEY
    return {
        "category_context" : category_context,
    } 
register.inclusion_tag("category/partial/row.html")(display_category_row)

def display_note_row(note_context):
    return {
        "note_context" : note_context['note'],
        "entity_context" : note_context['entity'],
    } 
register.inclusion_tag("note/partial/row.html")(display_note_row)

def count(value):
    if value == None:
        return 0
    return len(value)
register.filter(count)

def display_paginator(paginator):
    return {
        "paginator" : paginator,
    }
register.inclusion_tag("partial_paginator.html")(display_paginator)

