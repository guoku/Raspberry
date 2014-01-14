# coding=utf-8
from django import template


register = template.Library()


def display_note_item(note):
    return {
        'note_context' : note['note_context'],
        'creator_context' : note['creator_context'],
        'user_context' : note['user_context']
    }

register.inclusion_tag("entity/entity_note.html")(display_note_item)