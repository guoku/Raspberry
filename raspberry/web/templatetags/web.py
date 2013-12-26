# coding=utf-8

from django import template
import datetime
from base.note import Note
from base.user import User

register = template.Library()


def display_note(note_context, creator_context, user_context):
    _comment_id_list = note_context['comment_id_list']
    _comment_list = []

    for _comment_id in _comment_id_list:
        _note = Note(note_context['note_id'])
        _comment_context = _note.read_comment(_comment_id)
        _comment_context['creator_context'] = User(_comment_context['creator_id']).read()
        _comment_list.append(_comment_context)

    return {
        'note_context': note_context,
        'creator_context': creator_context,
        'user_context': user_context,
        'comment_list': _comment_list
    }

register.inclusion_tag("main/partial/display_note.html")(display_note)