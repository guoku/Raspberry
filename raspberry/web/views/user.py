# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from utils.paginator import Paginator
from util import *
from base.user import User
from base.category import Old_Category
from base.entity import Entity
from base.note import Note
from base.models import NoteSelection
from base.tag import Tag


def user_index(request, user_id):
    return user_likes(request, user_id)


TEMPLATE = 'user/index.html'


def user_likes(request, user_id, template=TEMPLATE):
    _c = request.GET.get('c', None)
    _p = request.GET.get('p', None)

    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    _curr_cat_id = 0

    if _c is not None:
        _c = int(_c)
        if int(_c) == 0:
            _c = None
        _curr_cat_id = _c

    _old_category_list = Old_Category.find()[0:12]

    # TODO
    # _entity_id_list = _query_user.find_like_entity(None, offset=0, count=30)
    # 没数据 用精选模拟
    _entity_list = []

    for _ns in NoteSelection.objects.all()[0:30]:
        _entity_id = _ns['entity_id']
        _entity_context = Entity(_entity_id).read()
        _entity_context['already_like'] = user_already_like_entity(request.user.id, _entity_id)
        _entity_list.append(_entity_context)

    return render_to_response(
        template,
        {
            'content_tab' : 'like',
            'user_context' : _user_context,
            'query_user_context' : _query_user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed,
            'category_list' : _old_category_list,
            'curr_cat_id' : _curr_cat_id,
            'entity_list' : _entity_list
        },
        context_instance=RequestContext(request)
    )


def user_posts(request, user_id, template=TEMPLATE):
    # TODO 是否需要?

    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    return render_to_response(
        template,
        {
            'content_tab' : 'post',
            'user_context' : _user_context,
            'query_user_context' : _query_user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed
        },
        context_instance=RequestContext(request)
    )


def user_notes(request, user_id, template=TEMPLATE):
    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    _p = int(request.GET.get('p', 1))

    _total_count = Note.count(creator_set=[user_id])
    _count_in_one_page = 30
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_p, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _note_id_list = Note.find(creator_set=[user_id], offset=_offset, count=_count_in_one_page)
    else:
        _note_id_list = Note.find(creator_set=[user_id], offset=0, count=_total_count)

    _note_list = []

    for _note in _note_id_list:
        _note_context = Note(_note).read()
        _creator_context = User(user_id).read()
        _entity_context = Entity(_note_context['entity_id']).read()

        _already_like = user_already_like_entity(request.user.id, _entity_context['entity_id'])

        _note_list.append(
            {
                'entity_context' : _entity_context,
                'note_context' : _note_context,
                'creator_context' : _creator_context,
                'already_like' : _already_like
            }
        )

    return render_to_response(
        template,
        {
            'content_tab' : 'note',
            'user_context' : _user_context,
            'query_user_context' : _query_user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed,
            'note_list' : _note_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_tags(request, user_id, template=TEMPLATE):
    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    _p = int(request.GET.get('p', 1))

    _tag_stat_list = Tag.user_tag_stat(user_id)
    _count_in_one_page = 5
    _total_count = len(_tag_stat_list)
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_p, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _tag_stat_list = _tag_stat_list[_offset: _offset + _count_in_one_page]

    _tag_list = []

    for _tag_stat in _tag_stat_list:
        _tag_id = _tag_stat['tag_id']
        _tag = _tag_stat['tag']
        _entity_list = []

        for _id in Tag.find_user_tag_entity(user_id, _tag):
            _entity_context = Entity(_id).read()
            _entity_context['already_like'] = user_already_like_entity(request.user.id, _id)
            _entity_list.append(_entity_context)

        _tag_list.append({
            'tag' : _tag,
            'tag_id' : _tag_id,
            'entity_list' : _entity_list
        })

    return render_to_response(
        template,
        {
            'content_tab' : 'tag',
            'user_context' : _user_context,
            'query_user_context' : _query_user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed,
            'tag_list' : _tag_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_followings(request, user_id, template=TEMPLATE):
    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    _p = request.GET.get('p', 1)

    _following_id_list = _query_user.read_following_user_id_list()
    _total_count = len(_following_id_list)
    _count_in_one_page = 30
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_p, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _following_id_list = _following_id_list[_offset: _offset + _count_in_one_page]

    _following_list = []

    for _id in _following_id_list:
        _f_user_context = User(_id).read()
        _f_user_context['is_user_followed'] = _user.is_following(_id)
        _following_list.append(_f_user_context)

    return render_to_response(
        template,
        {
            'content_tab' : 'following',
            'user_context' : _user_context,
            'query_user_context' : _query_user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed,
            'user_list' : _following_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


def user_fans(request, user_id, template=TEMPLATE):
    _user = User(request.user.id)
    _user_context = _user.read()

    _query_user_id = int(user_id)
    _query_user = User(_query_user_id)
    _query_user_context = _query_user.read()

    _is_user_self = (request.user.id == _query_user_id)
    _is_user_followed = _user.is_following(_query_user_id)

    _p = request.GET.get('p', 1)

    _fans_id_list = _query_user.read_fan_user_id_list()
    _total_count = len(_fans_id_list)
    _count_in_one_page = 30
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_p, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _fans_id_list = _fans_id_list[_offset: _offset + _count_in_one_page]

    _fans_list = []

    for _id in _fans_id_list:
        _f_user_context = User(_id).read()
        _f_user_context['is_user_followed'] = _user.is_following(_id)
        _fans_list.append(_f_user_context)

    return render_to_response(
        template,
        {
            'content_tab' : 'fan',
            'user_context' : _user_context,
            'is_user_self' : _is_user_self,
            'is_user_followed' : _is_user_followed,
            'query_user_context' : _query_user_context,
            'user_list' : _fans_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )


@login_required
def follow(request, user_id):
    _followee_id = int(user_id)
    _user = User(request.user.id)

    if _user.is_following(_followee_id):
        _user.unfollow(_followee_id)
        return HttpResponse('0')
    else:
        _user.follow(_followee_id)
        return HttpResponse('1')