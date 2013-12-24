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
    _result = 0

    if request.method == 'POST':
        _user_id = request.user.id
        _entity = Entity(entity_id)

        if _entity.like_already(_user_id):
            _entity.unlike(_user_id)
        else:
            _entity.like(_user_id)
        _result = 1

    return HttpResponse(_result)


@login_required
def add_note(request, entity_id):
    if request.method == 'POST':
        _creator_id = request.user.id
        _note_text = request.GET.get('note_text', None)
        _entity = Entity(entity_id)

        _note = _entity.add_note(_creator_id, _note_text)


@login_required
def del_note(request, entity_id):
    pass