# coding=utf8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from mobile.lib.http import SuccessJsonResponse 
from mobile.models import Session_Key
from models import Player
from weibo import APIClient
from web import sina_utils
import time

def main(request, template='main.html'):
    _session = request.POST.get('session', '')
    return render_to_response(
        template, 
        {
            'session' : 'abc' 
        }, 
        context_instance=RequestContext(request)
    )

def roll(request):
    _session = request.POST.get('session', None)
    _token = request.POST.get('token', None)
    return SuccessJsonResponse({ 'code': 5 })
     



def share_to_sina_weibo(request):
    _token = request.GET.get('token', None)
    if _token == '' or _token == None:
        request.session['auth_source'] = "lotto"
        return HttpResponseRedirect(sina_utils.get_login_url())
    
    print '...'
    return HttpResponseRedirect(reverse('lotto_main'))

