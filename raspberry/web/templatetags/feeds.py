from django.utils.log import getLogger
from django import template

from base.note import Note
from base.entity import Entity
from base.user import User
# from base.item import Item, JDItem

register = template.Library()
log = getLogger('django')

def display_feed_item(obj):
    _note_id = obj.note_id
    _note_context = Note(_note_id).read()
    _creator_context = User(_note_context['creator_id']).read()
    _entity_id = obj.entity_id
    _entity_context = Entity(_entity_id).read()

    return {
        'note_context':_note_context,
        'entity_context':_entity_context,
        'creator_context':_creator_context,
    }
register.inclusion_tag("feeds/partial/note_desc.html")(display_feed_item)
__author__ = 'edison7500'
