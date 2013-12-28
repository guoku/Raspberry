# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

from base.entity import Entity


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
def update_note(request, entity_id):
    if request.method == 'POST':
        _note_text = request.POST.get('note_text', None)
        _note_id = request.POST.get('note_id', None)

        if _note_id is not None and _note_text is not None and len(_note_text) > 0:
            _entity = Entity(int(entity_id))
            _entity.update_note(_note_id, note_text=_note_text)

            return HttpResponse('1')


@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        # TODO
        # return HttpResponse('1')
        pass