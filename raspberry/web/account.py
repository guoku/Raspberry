#coding=utf-8

from django.conf import settings
from django.contrib import messages

from django.shortcuts import render_to_response 
from django.contrib.auth.decorators import login_required

import taobao_utils
@login_required
def bind_taobao(request):
    request.session['bind_taobao_next_url'] = request.GET.get('next', None)
    request.session['back_to_url'] = reverse('web.views.bind_taobao_check')
    return HttpResponseRedirect(taobao_api.get_login_url())

def taobao_auth(request):
    return HttpResponseRedirect(taobao_utils.auth(request))

def bind_taobao_check(request):
        

