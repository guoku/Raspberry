# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.note import Note
from base.entity import Entity
from base.user import User


def detail(request, entity_id, template='detail/detail.html'):
    _entity_id = entity_id
    _entity_context = Entity(_entity_id).read()

    _all_note_id = Note.find(entity_id=_entity_id)
    _note_list = []

    for _note_id in _all_note_id:
        _note_context = Note(_note_id).read()
        _note_list.append({
            'note_context': _note_context,
            'creator_context': User(_note_context['creator_id']).read()
        })

    return render_to_response(template,
        {
            'entity_context': _entity_context,
            'note_list': _note_list
        },
        context_instance=RequestContext(request)
    )