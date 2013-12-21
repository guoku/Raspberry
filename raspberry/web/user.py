# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def login(request, template='user/login.html'):
    if request.method == 'GET':
        return render_to_response(template, {

        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def register(request, template='user/register.html'):
    if request.method == 'GET':
        return render_to_response(template, {

        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')