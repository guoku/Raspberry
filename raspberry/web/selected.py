# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def selected(request):
    _test = "Hello World"

    return render_to_response('selected/selected.html',
        {
            'test': _test
        },
        context_instance=RequestContext(request)
    )