#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
from taobaoapi.utils import load_taobao_item_info_from_api
from taobaoapi.client import TaobaoApiClient
import HTMLParser
import re 
import datetime
import time
import json

from base.entity import Entity 
from base.note import Note
from base.user import User
from utils.paginator import Paginator


@login_required
def note_list(request):
    _page_num = int(request.GET.get("p", "1"))
    _note_count = Note.count()
    _paginator = Paginator(_page_num, 30, _note_count)
    _note_id_list = Note.find(
        offset = _paginator.offset,
        count = _paginator.count_in_one_page,
    )
        
    _note_context_list = []
    for _note_id in _note_id_list:
        _note = Note(_note_id)
        _note_context = _note.read()
        _entity_id = _note_context['entity_id'] 
        _entity_context = Entity(_entity_id).read() 
        _note_context_list.append({
            'entity' : _entity_context,
            'note' : _note_context
        })
        
    return render_to_response( 
        'note/list.html', 
        {
            'active_division' : 'note',
            'note_context_list' : _note_context_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )


@login_required
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
            },
            context_instance = RequestContext(request)
        )
