# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from base.tag import Tag
from utils.http import JSONResponse


@login_required
def tag_suggest(request):
    _prefix = request.GET.get("prefix", None)
    if _prefix != None and len(_prefix) > 0:
        _tag_prefix_index = Tag.read_tag_prefix_index()
        if _tag_prefix_index.has_key(_prefix):
            _rslt = _tag_prefix_index[_prefix][0:5]
    else:
        _rslt = []
        _user_latest_tag_list = Tag.read_user_latest_tag_list(request.user.id)
        if _user_latest_tag_list == None or len(_user_latest_tag_list) == 0:
            _tag_prefix_index = Tag.read_tag_prefix_index()
            _rslt = _tag_prefix_index[0:5] 
        else:
            _rslt = _user_latest_tag_list[0:5]
    
    return JSONResponse(data=_rslt)

        
