# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
import json

from base.note import Note
from base.user import User
from share.tasks import DeleteEntityNoteCommentTask, PokeEntityNoteTask, DepokeEntityNoteTask


@login_required
def poke_note(request, note_id, target_status):
    if request.method == 'POST':
        _request_user_id = request.user.id 
        if target_status == '1':
            PokeEntityNoteTask.delay(note_id, _request_user_id)
            return HttpResponse('1')
        else:
            DepokeEntityNoteTask.delay(note_id, _request_user_id)
            return HttpResponse('0')


def get_comments(request, note_id, template='note/note_comment_list.html'):
    _user_context = User(request.user.id)
    _note = Note(note_id)
    _note_context = _note.read()
    _comment_id_list = _note_context['comment_id_list']
    _comment_list = []

    _ret = {
        'status' : '0',
        'msg' : ''
    }

    for _c_id in _comment_id_list:
        _comment_context = _note.read_comment(_c_id)
        _creator_id = _comment_context['creator_id']
        _creator_context = User(_creator_id).read()
        _reply_to_user_id = _comment_context['reply_to_user_id']

        if _reply_to_user_id is not None:
            _nickname = User(_reply_to_user_id).read()['nickname']
            _comment_context['reply_to_user_nickname'] = _nickname

        _comment_list.append(
            {
                'comment_context' : _comment_context,
                'creator_context' : _creator_context,
                'note_context' : _note_context,
                'user_context' : _user_context
            }
        )

    _t = loader.get_template(template)
    _c = RequestContext(request, {
        'comment_list': _comment_list,
        'note_context': _note_context,
    })
    _data = _t.render(_c)

    _ret = {
        'status': '1',
        'data': _data
    }

    return HttpResponse(json.dumps(_ret))


@login_required
def add_comment(request, note_id, template='note/note_comment.html'):
    if request.method == 'POST':
        _user_context = User(request.user.id).read()
        _creator_id = request.user.id
        _comment_text = request.POST.get('comment_text', None)
        _reply_to_user_id = request.POST.get('reply_to_user_id', None)
        _reply_to_comment_id = request.POST.get('reply_to_comment_id', None)

        _ret = {
            'status' : '0',
            'msg' : ''
        }

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
            _new_comment_id = _note.add_comment(_comment_text, _creator_id, reply_to_comment_id=_reply_to_comment_id,
                                                reply_to_user_id=_reply_to_user_id)
            _comment_context = _note.read_comment(_new_comment_id)

            if _reply_to_user_id is not None:
                _nickname = User(_reply_to_user_id).read()['nickname']
                _comment_context['reply_to_user_nickname'] = _nickname

            _creator_context = User(_creator_id).read()

            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'comment_context': _comment_context,
                'creator_context': _creator_context,
                'user_context': _user_context
            })
            _data = _t.render(_c)

            _ret = {
                'status': '1',
                'data': _data
            }

        return HttpResponse(json.dumps(_ret))



@login_required
def delete_comment(request, note_id, comment_id):
    if request.method == 'POST':
        _note = Note(note_id)
        _note_context = _note.read()
        _comment_context = _note.read_comment(comment_id)
        _user_id = request.user.id

        # 判断当前用户是否具有删除权限
        if _comment_context['creator_id'] == _user_id or _note_context['creator_id'] == _user_id:
            _note.del_comment(comment_id)

            return HttpResponse('1')
