# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from util import get_request_user_context
from base.user import User
from base.category import Old_Category
from base.entity import Entity
from base.note import Note


def _get_user_basic_info(user_id):
    _info = {}
    return _info


def index(request, user_id):
    return likes(request, user_id)


def likes(request, user_id, template='user/index.html'):
    _c = request.GET.get('c', None)
    _p = request.GET.get('p', None)
    _curr_cat_id = 0

    if _c is not None:
        if _c == int(0):
            _c = None
        _curr_cat_id = int(_c)

    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    _old_category_list = Old_Category.find()[0:12]

    _entity_id_list = _query_user.find_like_entity(None, offset=0, count=30)
    _entity_list = []

    for _entity_id in _entity_id_list:
        _entity_context = Entity(_entity_id).read()
        _entity_list.append(_entity_context)

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 1,
            'query_user_context' : _query_user_context,
            'category_list' : _old_category_list,
            'curr_cat_id' : _curr_cat_id,
            'entity_list' : _entity_list
        },
        context_instance=RequestContext(request)
    )


def posts(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 2,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def notes(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    _note_id_list = Note.find(creator_set=[user_id], offset=0, count=30)
    _note_list = []

    for _note in _note_id_list:
        _note_context = Note(_note).read()
        _creator_context = User(user_id).read()
        _entity_context = Entity(_note_context['entity_id']).read()

        _note_list.append(
            {
                'entity_context' : _entity_context,
                'note_context' : _note_context,
                'creator_context' : _creator_context
            }
        )

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 3,
            'query_user_context' : _query_user_context,
            'note_list' : _note_list
        },
        context_instance=RequestContext(request)
    )


def tags(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 4,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def followings(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 5,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def fans(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 6,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )