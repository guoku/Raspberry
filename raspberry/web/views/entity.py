# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

from base.entity import Entity
from base.entity import Note
from base.user import User


@login_required
def new_entity(request, template='entity/create_entity.html'):
    _user = User(request.user.id)
    _user_context = _user.read()

    if request.method == 'GET':
        return render_to_response(
            template,
            {
                'method' : 0,
                'user_context' : _user_context
            },
            context_instance = RequestContext(request)
        )
    else:
        return render_to_response(
            template,
            {
                'method' : 1,
                'user_context' : _user_context
            },
            context_instance = RequestContext(request)
        )


@login_required
def like_entity(request, entity_id):
    if request.method == 'POST':
        _user_id = request.user.id
        _entity = Entity(int(entity_id))

        if _entity.like_already(_user_id):
            _entity.unlike(_user_id)
            return HttpResponse('0')
        else:
            _entity.like(_user_id)
            return HttpResponse('1')


@login_required
def add_note(request, entity_id):
    if request.method == 'POST':
        _note_text = request.POST.get('note_text', None)

        if _note_text is not None and len(_note_text) > 0:
            try:
                _entity = Entity(int(entity_id))
                _entity.add_note(request.user.id, _note_text)
            except:
                pass

            return HttpResponse('1')


@login_required
def update_note(request, entity_id, note_id):
    if request.method == 'POST':
        _note_text = request.POST.get('note_text', None)

        if _note_text is not None and len(_note_text) > 0:
            _note_context = Note(note_id).read()

            if _note_context['creator_id'] == request.user.id:
                _entity = Entity(entity_id)
                _entity.update_note(note_id, note_text=_note_text)

                return HttpResponse('1')


@login_required
def delete_note(request, entity_id, note_id):
    if request.method == 'POST':
        pass