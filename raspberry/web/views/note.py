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
    if request.method == 'POST':
        _user_id = request.user.id
        _note = Note(note_id)

        if _note.poke_already(_user_id):
            _note.depoke(note_id)
            return HttpResponse('0')
        else:
            _note.poke(note_id)
            return HttpResponse('1')


@login_required
def add_comment(request, note_id):
    if request.method == 'POST':
        _creator_id = request.user.id
        _comment_text = request.POST.get('comment_text', None)
        _reply_to_user_id = request.POST.get('reply_to_user_id', None)
        _reply_to_comment_id = request.POST.get('reply_to_comment_id', None)

        if _comment_text is not None and len(_comment_text) > 0:
            if _reply_to_comment_id is not None:
                if len(_reply_to_user_id) > 0:
                    _reply_to_comment_id = int(_reply_to_comment_id)
                else:
                    _reply_to_comment_id = None

            if _reply_to_user_id is not None:
                if len(_reply_to_user_id) > 0:
                    _reply_to_user_id = int(_reply_to_user_id)
                else:
                    _reply_to_user_id = None

            _note = Note(int(note_id))
            _note.add_comment(_comment_text, _creator_id, reply_to_comment_id=_reply_to_comment_id,
                              reply_to_user_id=_reply_to_user_id)

            return HttpResponse('1')


@login_required
def delete_comment(request, note_id):
    if request.method == 'POST':
        _comment_id = request.POST.get('comment_id', None)

        if _comment_id is not None:
            _note = Note(note_id)
            _note.del_comment(int(_comment_id))

            return HttpResponse('1')