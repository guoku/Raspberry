# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from util import get_request_user_context
from base.user import User
from base.category import Old_Category
from base.entity import Entity
from base.note import Note
from base.models import NoteSelection


def user_index(request, user_id):
    return user_likes(request, user_id)


TEMPLATE = 'user/index.html'


def user_likes(request, user_id, template=TEMPLATE):
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

    # TODO
    _entity_id_list = _query_user.find_like_entity(None, offset=0, count=30)

    # 没数据 用精选模拟 TODO
    _entity_id_list = [entity['entity_id'] for entity in NoteSelection.objects.all()[0:30]]

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


def user_posts(request, user_id, template=TEMPLATE):
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


def user_notes(request, user_id, template=TEMPLATE):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    # TODO
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


def user_tags(request, user_id, template=TEMPLATE):
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


def user_followings(request, user_id, template=TEMPLATE):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    # TODO paginate
    _following_id_list = _query_user.read_following_user_id_list()[0:30]
    _following_list = []

    for _f_id in _following_id_list:
        _f_context = User(_f_id).read()
        _following_list.append(_f_context)

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 5,
            'query_user_context' : _query_user_context,
            'user_list' : _following_list
        },
        context_instance=RequestContext(request)
    )


def user_fans(request, user_id, template=TEMPLATE):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    # TODO
    _fans_id_list = _query_user.read_fan_user_id_list()[0:30]
    _fans_list = []

    for _f_id in _fans_id_list:
        _f_context = User(_f_id).read()
        _fans_list.append(_f_context)


    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 6,
            'query_user_context' : _query_user_context,
            'user_list' : _fans_list
        },
        context_instance=RequestContext(request)
    )