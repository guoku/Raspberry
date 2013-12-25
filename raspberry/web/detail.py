# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.note import Note
from base.entity import Entity
from base.user import User


def detail(request, entity_hash, template='detail/detail.html'):
    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    _entity_context = Entity(_entity_id).read()
    _all_note_id = Note.find(entity_id=_entity_id)

    _note_list = []
    _selected_note = {}

    for _note_id in _all_note_id:
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()

        if _note_context['selector_id'] is None:
            _note_list.append({
                'note_context': _note_context,
                'creator_context': _creator_context
            })
        else:
            _selected_note['note_context'] = _note_context
            _selected_note['creator_context'] = _creator_context

    return render_to_response(template,
        {
            'entity_context': _entity_context,
            'note_list': _note_list,
            'selected_note': _selected_note
        },
        context_instance=RequestContext(request)
    )