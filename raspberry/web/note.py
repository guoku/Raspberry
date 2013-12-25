# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

from base.note import Note


@login_required
def poke_note(request, note_id):
    _result = 0

    if request.method == 'POST':
        _user_id = request.user.id
        _note = Note(note_id)

        if _note.poke_already(_user_id):
            _note.depoke(note_id)
        else:
            _note.poke(note_id)
        _result = 1

    return HttpResponse(json.dumps(_result))


@login_required
def add_comment(request, note_id):
    pass


@login_required
def del_comment(request, note_id):
    pass