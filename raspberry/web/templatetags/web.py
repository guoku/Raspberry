# coding=utf-8

from django import template
import datetime
from base.note import Note
from base.user import User

register = template.Library()


def display_note(note_context, creator_context, display_comment=False):
    _comment_list = None

    if display_comment:
        _comment_id_list = note_context['comment_id_list']
        _comment_list = []

        for _comment_id in _comment_id_list:
            _note = Note(note_context['note_id'])
            _comment = _note.read_comment(_comment_id)
            _comment['creator'] = User(_comment['creator_id']).read()
            _comment_list.append(_comment)

    return {
        'note': note_context,
        'creator': creator_context,
        'comment_list': _comment_list
    }


register.inclusion_tag("main/partial/display_note.html")(display_note)