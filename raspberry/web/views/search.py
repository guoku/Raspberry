# coding=utf-8
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.template import loader
# import json

from util import *
from utils.paginator import Paginator
from base.user import User
# from base.category import Old_Category
from base.entity import Entity
# from base.note import Note
from base.models import NoteSelection
from base.tag import Tag


def search(request, template='search/search.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    _keyword = request.GET.get('q', None)
    _group = request.GET.get('g', 'e')  # e->entity, u->user, t->tag
    _page = request.GET.get('p', 1)

    _entity_list = []
    _user_list = []
    _tag_list = []

    # TODO
    # entity example ------------------------
    _entity_id_list = [x['entity_id'] for x in NoteSelection.objects[0:30]]

    for _e_id in _entity_id_list:
        _entity_context = Entity(_e_id).read()
        _entity_context['is_user_already_like'] = user_already_like_entity(request.user.id, _e_id)
        _entity_list.append(_entity_context)

    # TODO
    # user example --------------------------
    _user_id_list = []
    _total_count = len(_user_id_list)
    _count_in_one_page = 20
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_page, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _following_id_list = _user_id_list[_offset: _offset + _count_in_one_page]

    for _id in _user_id_list:
        _f_user_context = User(_id).read()
        _f_user_context['is_user_already_follow'] = False

        if _user is not None:
            _f_user_context['is_user_already_follow'] = _user.is_following(_id)

        _user_list.append(_f_user_context)

    # TODO
    # tag example -------------------------------
    _tag_stat_list = []
    _count_in_one_page = 20
    _total_count = len(_tag_stat_list)
    _paginator = None

    if _total_count > _count_in_one_page:
        _paginator = Paginator(_page, _count_in_one_page, _total_count)
        _offset = _paginator.offset
        _tag_stat_list = _tag_stat_list[_offset: _offset + _count_in_one_page]

    for _tag_stat in _tag_stat_list:
        _tag_id = _tag_stat['tag_id']
        _tag = _tag_stat['tag']
        _user_id = 12  # TODO
        _entity_id_list = Tag.find_user_tag_entity(_user_id, _tag)
        _entity_count = len(_entity_id_list)
        _entity_list = [Entity(x).read() for x in _entity_id_list[:4]]

        _tag_list.append({
            'tag' : _tag,
            'tag_id' : _tag_id,
            'entity_list' : _entity_list,
            'entity_count' : _entity_count
        })

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'keyword' : _keyword,
            'group' : _group,
            'entity_list' : _entity_list,
            'user_list' : _user_list,
            'tag_list' : _tag_list,
            'paginator' : _paginator
        },
        context_instance=RequestContext(request)
    )
