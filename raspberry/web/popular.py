# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def popular(request, template='popular/popular.html'):
    return render_to_response(template,
        {

        },
        context_instance=RequestContext(request)
    )