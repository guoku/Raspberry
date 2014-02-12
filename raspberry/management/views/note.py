#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger
# from urlparse import urlparse
# import HTMLParser
# import re
import datetime
import time
import json

from base.entity import Entity
from base.note import Note
from base.user import User
from management.tasks import ArrangeSelectionTask
from utils.authority import staff_only
from utils.paginator import Paginator

log = getLogger('django')

@login_required
@staff_only
def arrange_selection(request):
    if request.method == 'GET':
        _t_start = datetime.datetime.now() + datetime.timedelta(days = 1)
        _year = _t_start.year
        _month = _t_start.month
        _date = _t_start.day
        _start_time = "%d-%d-%d 8:00:00"%(_year, _month, _date)

        _pending_note_count = Note.count(pending_selection = True)
        return render_to_response(
            'note/arrange.html',
            {
                'active_division' : 'note',
                'pending_note_count' : _pending_note_count,
                'start_time' : _start_time
            },
            context_instance = RequestContext(request)
        )
    else:
        _count = int(request.POST.get("count", None))
        _start_time = request.POST.get("start_time")
        _start_time = datetime.datetime.strptime(_start_time, "%Y-%m-%d %H:%M:%S")
        _interval = int(request.POST.get("interval", None))
        ArrangeSelectionTask.delay(
            select_count = _count,
            start_time = _start_time,
            interval_secs = _interval
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])



@login_required
@staff_only
def note_list(request):
    _selection = request.GET.get("selection", None)
    _select_entity_id = request.GET.get("entity_id", None)
    _nav_filter = 'all'
    _sort_by = None
    _para = {}
    if _selection == 'only':
        _selection = 1
        _nav_filter = 'selection_only'
        _sort_by = 'selection_post_time'
        _para['selection'] = 'only'
    elif _selection == 'none':
        _selection = -1
        _nav_filter = 'selection_none'
        _para['selection'] = 'none'
    else:
        _selection = 0

    _freezed = request.GET.get("freeze", None)
    if _freezed == '1':
        _status = -1
        _nav_filter = 'freezed'
        _para['freeze'] = '1'
    else:
        _status = 1

    _page_num = int(request.GET.get("p", "1"))
    if not _select_entity_id:
        _note_count = Note.count(selection = _selection, status = _status)
        _paginator = Paginator(_page_num, 30, _note_count, _para)
        _note_id_list = Note.find(
            offset = _paginator.offset,
            count = _paginator.count_in_one_page,
            selection = _selection,
            status = _status,
            sort_by = _sort_by
        )
    else:
        _note_count = Note.count(entity_id=_select_entity_id)
        _paginator = Paginator(_page_num, 30, _note_count, _para)
        _note_id_list = Note.find(entity_id=_select_entity_id)

    _context_list = []
    # log.info(_note_id_list)
    for _note_id in _note_id_list:
        try:
            _note = Note(_note_id)
            _note_context = _note.read()
            _entity_id = _note_context['entity_id']
            _entity_context = Entity(_entity_id).read()
            # log.info(_entity_context)
            log.info( _note_context['post_time'] )
            if _note_context['post_time'] is None:
                _is_future = 0
            else:
                post_time = time.mktime( _note_context['post_time'].timetuple() )
                bench_time = time.mktime( datetime.datetime(2100, 1, 1).timetuple() )
            # log.info( bench_time, post_time )
            # if _note_context['post_time'] == datetime.datetime(2100, 1, 1):
                if post_time == bench_time:
                    _is_future = 1
                # else:
                #     _is_future = 0
            # log.info(_note_context['post_time'])
            _context_list.append({
                'entity': _entity_context,
                'note': _note_context,
                'creator': User(_note_context['creator_id']).read(),
                'is_future': _is_future,
            })
        except Exception, e:
            log.error("Error: %s" % e.message)
        # log.info(_context_list)

    return render_to_response( 
        'note/list.html',
        {
            'active_division' : 'note',
            'nav_filter' : _nav_filter,
            'context_list' : _context_list,
            'paginator' : _paginator,
            'select_entity_id': _select_entity_id
        },
        context_instance = RequestContext(request)
    )


@login_required
@staff_only
def freeze_note(request, note_id):
    if request.method == 'GET':
        _note = Note(note_id)
        _entity_id = _note.get_entity_id()
        _entity = Entity(_entity_id)
        _entity.update_note(
            note_id = note_id,
            weight = -1
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])



@login_required
@staff_only
def edit_note(request, note_id):
    if request.method == 'GET':
        _note_context = Note(note_id).read()
        _entity_context = Entity(_note_context['entity_id']).read()
        return render_to_response(
            'note/edit.html',
            {
                'active_division' : 'note',
                'entity_context' : _entity_context,
                'note_context' : _note_context,
                'creator' : User(_note_context['creator_id']).read()
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _note_text = request.POST.get("note", None)
        _weight = int(request.POST.get("weight", '0'))
        _note = Note(note_id)
        _entity_id = _note.get_entity_id()
        _entity = Entity(_entity_id)
        _entity.update_note(
            note_id = note_id,
            note_text = _note_text, 
            weight = _weight
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@staff_only
def update_note_selection_info(request, entity_id, note_id):
    _post_time = request.POST.get("post_time")
    _post_time = datetime.datetime.strptime(_post_time, "%Y-%m-%d %H:%M:%S")
    _request_user_id = request.user.id
    _selected_time = datetime.datetime.now()
    
    Entity(entity_id).update_note_selection_info(
        note_id = note_id,
        selector_id = _request_user_id,
        selected_time = _selected_time,
        post_time = _post_time
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    




@login_required
@staff_only
def post_selection_instant(request, entity_id, note_id):
    _request_user_id = request.user.id
    _selected_time = datetime.datetime.now()
    _post_time = datetime.datetime.now()
    Entity(entity_id).update_note_selection_info(
        note_id = note_id,
        selector_id = _request_user_id,
        selected_time = _selected_time,
        post_time = _post_time
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@staff_only
def post_selection_delay(request, entity_id, note_id):
    _request_user_id = request.user.id
    _selected_time = datetime.datetime.now()
    _post_time = datetime.datetime(2100, 1, 1)
    _entity_id = int(entity_id)
    _note_id = int(note_id)
    Entity(_entity_id).update_note_selection_info(
        note_id = _note_id,
        selector_id = _request_user_id,
        selected_time = _selected_time,
        post_time = _post_time
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
