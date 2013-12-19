# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.paginator import Paginator
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.user import User


def selection(request):
    _page_num = int(request.GET.get('p', 1))
    _category_id = request.GET.get('c', None)

    _hdl = NoteSelection.objects.all()
    if _category_id is not None:
        _hdl = NoteSelection.objects.filter(neo_category_id=_category_id)

    _total_count = _hdl.count()
    _count_in_one_page = 25
    _paginator = Paginator(_page_num, _count_in_one_page, _total_count)

    _hdl.order_by('-post_time')
    _offset = _paginator.offset
    _note_selections = _hdl[_offset: _offset + _count_in_one_page]

    _selections = []
    _note_list = []

    for note_selection in _note_selections:
        _entity_id = note_selection['entity_id']
        _note_id = note_selection['note_id']
        _selector_id = note_selection['selector_id']

        _entity = Entity(_entity_id).read()
        _note = Note(_note_id).read()
        _creator = User(_selector_id).read()

        _all_note = Note.find(entity_id=_entity_id)
        for _note_id in _all_note:
            _note = Note(_note_id).read()
            _note_list.append({
                'entity': Entity(_note['entity_id']).read(),
                'note': _note,
                'creator': User(_note['creator_id']).read()
            })

        _selections.append({
            'entity': _entity,
            'note': _note,
            'creator': _creator
        })

    return render_to_response('selection/selection.html',
        {
            "selections": _selections,
            'note_list': _note_list
        },
        context_instance=RequestContext(request)
    )