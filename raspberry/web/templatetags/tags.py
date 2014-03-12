from django.utils.log import getLogger
from django import template
from base.tag import Tag

register = template.Library()
log = getLogger('django')

def trans_tag(value):
    tag_name = Tag.tag_name(value)

    return tag_name
register.filter(trans_tag)

__author__ = 'edison7500'
