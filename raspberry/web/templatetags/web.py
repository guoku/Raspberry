# coding=utf-8

from django import template
import datetime
from base.note import Note
from base.user import User

register = template.Library()


def display_note(note, entity_context, user_context):
    return {
        'note_context' : note['note_context'],
        'creator_context' : note['creator_context'],
        'comment_list' : note['comment_list'],
        'entity_context' : entity_context,
        'user_context' : user_context
    }

register.inclusion_tag("main/partial/display_note.html")(display_note)