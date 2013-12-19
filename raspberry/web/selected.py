# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.paginator import Paginator


def selected(request):
    _page = int(request.GET.get('p', 1))
    _category = request.GET.get('c', None)



    return render_to_response('selected/selected.html',
        {

        },
        context_instance=RequestContext(request)
    )