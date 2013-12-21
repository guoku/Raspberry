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


def selection(request, template='selection/selection.html'):
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

    _selections = []

    for note_selection in _note_selections:
        _entity_id = note_selection['entity_id']
        _note_id = note_selection['note_id']

        _entity_context = Entity(_entity_id).read()
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()

        _all_note_id = Note.find(entity_id=_entity_id)
        _note_list = []

        for _note_id_ in _all_note_id:
            if _note_id_ != _note_id:
                _note_context_ = Note(_note_id_).read()
                _note_list.append({
                    'note_context': _note_context_,
                    'creator_context': User(_note_context_['creator_id']).read()
                })

        _selections.append({
            'entity_context': _entity_context,
            'note_context': _note_context,
            'creator_context': _creator_context,
            'note_list': _note_list
        })

    return render_to_response(template,
        {
            'selections': _selections,
            'categories': _old_category_list,
            'curr_cat_title': _curr_cat_title
        },
        context_instance=RequestContext(request)
    )