#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
import HTMLParser
import re 
import datetime
import time
import json

from common.category import RBCategory
from common.candidate import RBCandidate
from common.entity import RBEntity
from common.note import RBNote
from common.user import RBUser


@login_required
def candidate_list(request):
    _group_id = request.GET.get("gid", None)
    if _group_id == None:
        _category_groups = RBCategory.allgroups()
        _category_id = request.GET.get("cid", None)
        if _category_id != None: 
            _category_id = int(_category_id)
            _category_context = RBCategory(_category_id).read()
            _category_group_id = _category_context['group_id'] 
            _categories = RBCategory.find(group_id = _category_context['group_id'])
            for _category in _categories:
                _category['candidate_count'] = RBCandidate.count(_category['category_id'])
        else:
            _category_context = None
            _category_group_id = None
            _categories = None
        
        _filtering = 'all' 

        _pending_only = request.GET.get('pending', '0')
        if _pending_only == '0':
            _pending_only = False
        else:
            _pending_only = True
            _filtering = 'pending' 
        
        _approve_already = request.GET.get('approve', '0')
        if _approve_already == '0':
            _approve_already = False
        else:
            _approve_already = True
            _filtering = 'approve' 


        _candidate_id_list = RBCandidate.find(
            category_id = _category_id,
            pending_only = _pending_only,
            approve_already = _approve_already
        )
        _candidate_context_list = []
        for _candidate_id in _candidate_id_list: 
            _candidate_context = RBCandidate(_candidate_id).read()
            _note_context = RBNote(_candidate_context['note_id']).read()
            _creator_context = RBUser(_note_context['creator_id']).read()
            _candidate_context_list.append({
                'candidate' : _candidate_context,
                'note' : _note_context,
                'creator' : _creator_context
            })
        
        return render_to_response( 
            'candidate/list.html', 
            {
                'active_division' : 'candidate',
                'filtering' : _filtering, 
                'category_context' : _category_context,
                'category_groups' : _category_groups,
                'categories' : _categories,
                'category_group_id' : _category_group_id,
                'candidate_context_list' : _candidate_context_list,
            },
            context_instance = RequestContext(request)
        )
    else:
        _categories = RBCategory.find(group_id = int(_group_id))
        return HttpResponseRedirect(reverse('management.views.candidate_list') + '?cid=' + str(_categories[0]['category_id'])) 

@login_required
def edit_candidate(request, candidate_id):
    if request.method == 'GET':
        _candidate_context = RBCandidate(candidate_id).read()
        _note_context = RBNote(_candidate_context['note_id']).read()
        _creator_context = RBUser(_note_context['creator_id']).read()
        _category_list = RBCategory.find()
        return render_to_response( 
            'candidate/edit.html', 
            {
                'active_division' : 'candidate',
                'candidate_context' : _candidate_context,
                'category_list' : RBCategory.find(), 
                'note_context' : _note_context,
                'creator_context' : _creator_context,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _brand = request.POST.get('brand', None)
        _title = request.POST.get('title', None)
        _category_id = int(request.POST.get('category_id', '0'))
        _category_text = request.POST.get('category_text', None)
        _score = request.POST.get('score', '0')
        _note_text = request.POST.get('note_text', None)
        _weight = request.POST.get('weight', None)
        RBCandidate(candidate_id).update(
            category_id = _category_id, 
            category_text = _category_text, 
            brand = _brand, 
            title = _title, 
            score = _score, 
            note_text = _note_text,
            weight = _weight
        )
        return HttpResponseRedirect(reverse('management.views.edit_candidate', kwargs = { "candidate_id" : candidate_id }))
            
@login_required
def shift_candidate_to_entity(request, candidate_id):
    if request.method == 'POST':
        _entity_id = request.POST.get('entity_id', None)
        RBEntity(_entity_id).bind_note_from_candidate(candidate_id)
        return HttpResponseRedirect(reverse('management.views.edit_entity', kwargs = { "entity_id" : _entity_id }))
