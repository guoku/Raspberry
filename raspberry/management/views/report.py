#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import HTMLParser
import re 
import datetime
import time
import json

from base.report import Report, EntityReport, EntityNoteReport
from utils.paginator import Paginator

@login_required
def report_list(request):
    _page_num = int(request.GET.get("p", "1"))
    _paginator = Paginator(_page_num, 30, Report.objects.count())
    
    _report_context_list = []
    for _report in Report.objects.all().order_by('-created_time')[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        if isinstance(_report, EntityReport):
            _report_context_list.append({
                'type' : 'entity_report',
                'comment' : _report.comment,
                'entity_id' : _report.entity_id,
                'reporter_id' : _report.reporter_id
            })
        elif isinstance(_report, EntityNoteReport):
            _report_context_list.append({
                'type' : 'entity_note_report',
                'comment' : _report.comment,
                'note_id' : _report.note_id,
                'reporter_id' : _report.reporter_id
            })
    
    return render_to_response( 
        'report/list.html', 
        {
            'active_division' : 'report',
            'report_context_list' : _report_context_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )
