# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.paginator import Paginator
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.user import User
from base.category import Old_Category


def selection(request, template='main/selection.html'):
    _user = request.user
    _user_context = None

    if _user.id is not None:
        _user_context = User(_user.id).read()

    _page_num = int(request.GET.get('p', 1))
    _category_id = request.GET.get('c', None)

    _curr_cat_title = None
    _old_category_list = Old_Category.find()[0:12]

    if _category_id is None:
        _hdl = NoteSelection.objects.all()
    else:
        _hdl = NoteSelection.objects.filter(category_id=_category_id)

        for _old_cat in _old_category_list:
            if _old_cat['category_id'] == int(_category_id):
                _curr_cat_title = _old_cat['category_title']

    _total_count = _hdl.count()
    _count_in_one_page = 25
    _paginator = Paginator(_page_num, _count_in_one_page, _total_count)

    _hdl.order_by('-post_time')
    _offset = _paginator.offset
    _note_selections = _hdl[_offset: _offset + _count_in_one_page]

    _selection_list = []

    for _note_selection in _note_selections:
        _entity_id = _note_selection['entity_id']
        _entity = Entity(_entity_id)
        _note_id = _note_selection['note_id']

        _already_like = False

        if _user.id is not None:
            _already_like = _entity.like_already(_user.id)

        _entity_context = _entity.read()
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()

        _all_note_id = Note.find(entity_id=_entity_id)
        _note_list = []

        for _note_id_other in _all_note_id:
            if _note_id_other != _note_id:
                _note_context_other = Note(_note_id_other).read()
                _note_list.append(
                    {
                        'note_context' : _note_context_other,
                        'creator_context' : User(_note_context_other['creator_id']).read()
                    }
                )

        _selection_list.append(
            {
                'already_like' : _already_like,
                'entity_context' : _entity_context,
                'note_context' : _note_context,
                'creator_context' : _creator_context,
                'note_list' : _note_list
            }
        )

    return render_to_response(
        template,
        {
            'user' : _user,
            'user_context' : _user_context,
            'selection_list' : _selection_list,
            'category_list' : _old_category_list,
            'curr_cat_title' : _curr_cat_title
        },
        context_instance=RequestContext(request)
    )


def detail(request, entity_hash, template='main/detail.html'):
    _user = request.user
    _user_context = None

    if _user.id is not None:
        _user_context = User(_user.id).read()

    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    _entity_context = Entity(_entity_id).read()
    _all_note_id = Note.find(entity_id=_entity_id)

    _note_list = []
    _selected_note = {}
    _user_already_note = False

    for _note_id in _all_note_id:
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()

        if _creator_context['user_id'] == _user.id:
            _user_already_note = True

        # 判断是否是精选
        if _note_context['selector_id'] is None:
            _note_list.append(
                {
                    'note_context' : _note_context,
                    'creator_context' : _creator_context
                }
            )
        else:
            _selected_note['note_context'] = _note_context
            _selected_note['creator_context'] = _creator_context

    return render_to_response(
        template,
        {
            'user' : _user,
            'user_context' : _user_context,
            'entity_context' : _entity_context,
            'note_list' : _note_list,
            'selected_note' : _selected_note,
            'user_already_note' : _user_already_note
        },
        context_instance=RequestContext(request)
    )


def popular(request, template='main/popular.html'):
    _group = request.GET.get('group', 'daily')

    # generate_popular_entity()
    # _entity_list = read_popular_entity_from_cache(_group)['data']
    #
    # print(_entity_list)

    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )


def discover(request, template='main/discover.html'):
    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )
