# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger
from base.tag import Tag
from base.entity import Entity
from utils.http import JSONResponse
from utils.lib import get_client_ip
from utils.paginator import Paginator
from web.tasks import WebLogTask
import datetime

log = getLogger('django')

@login_required
def tag_suggest(request):
    _prefix = request.GET.get("prefix", None)
    _rslt = []
    if _prefix != None and len(_prefix) > 0:
        _tag_prefix_index = Tag.read_tag_prefix_index()
        if _tag_prefix_index.has_key(_prefix):
            _rslt = _tag_prefix_index[_prefix][0:5]
    else:
        _user_latest_tag_list = Tag.read_user_latest_tag_list(request.user.id)
        if _user_latest_tag_list != None or len(_user_latest_tag_list) > 0:
            _rslt = _user_latest_tag_list[0:5]
    
    return JSONResponse(data=_rslt)

        
def tag_detail(request, tag_hash, template="tag/tag_detail.html"):
    _start_at = datetime.datetime.now()
    _request_user_id = request.user.id if request.user.is_authenticated() else None 
    
    _tag_text = Tag.get_tag_text_from_hash(tag_hash)
    _entity_id_list = Tag.find_tag_entity(tag_hash)
    _page_num = request.GET.get('p', 1)
    _paginator = Paginator(_page_num, 24, len(_entity_id_list))
    
    _entities = [] 
    for _entity_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
        try:
            _entities.append(Entity(_entity_id).read())
        except Exception, e:
            pass
    
    _duration = datetime.datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds, 
        page='TAG', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'tag' : _tag_text, 
            'result_entities' : _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]
        },
    )
    
    return render_to_response(template,
        {
            "tag": _tag_text,
            "entities": _entities,
            "paginator" : _paginator
        },
        context_instance=RequestContext(request)
    )


def tag_origin(request, tag):
    _tag_hash = Tag.get_tag_hash_from_text(tag) 
    return HttpResponsePermanentRedirect(reverse('web_tag_detail', kwargs = { "tag_hash" : _tag_hash }))
