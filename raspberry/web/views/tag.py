# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from base.tag import Tag
from utils.http import JSONResponse


def tag_suggest(request):
    _prefix = request.GET.get("prefix", None)
    _tag_prefix_index = Tag.read_tag_prefix_index()
    if _prefix != None and len(_prefix) > 0:
        if _tag_prefix_index.has_key(_prefix):
            _rslt = _tag_prefix_index[_prefix][0:5]
    else:
        _rslt = []
    
    return JSONResponse(data=_rslt)

        
