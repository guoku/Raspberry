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
import datetime
import time

def _is_the_same_date(dt1, dt2):
    if dt1 == None or dt2 == None:
        return False
    if dt1.strftime('%Y-%m-%d') == dt2.strftime('%Y-%m-%d'):
        return True
    return False
    

def _cal_available_roll_count(share_count, roll_count, last_share_time):
    if last_share_time != None:
        if _is_the_same_date(last_share_time, datetime.datetime.now()): 
            _count = share_count - roll_count
            if _count < 0:
                _count = 0
            return _count
    return -1 

def main(request, template='main.html'):
    _session = request.GET.get('session', '')
    _token = request.GET.get('token', '')
    _infocode = request.GET.get('ifc', None)
    _count = -1 
    
    if _token != '' and _token != None:
        _player = Player.objects.get(token = _token)
        _count = _cal_available_roll_count(_player.share_count, _player.roll_count, _player.last_share_time) 
    
    return render_to_response(
        template, 
        {
            'count' : _count,
            'session' : _session, 
            'token' : _token,
            'infocode' : _infocode
        }, 
        context_instance=RequestContext(request)
    )

def roll(request):
    _token = request.GET.get('token', None)
    _player = Player.objects.get(token=_token)
    
    if not _is_the_same_date(_player.last_share_time, datetime.datetime.now()):
        return SuccessJsonResponse({ 'code': 5 })
    
    if _player.share_count <= _player.roll_count:
        return SuccessJsonResponse({ 'code': 4 })

    return SuccessJsonResponse({ 'code': 3 })
     

def share_to_sina_weibo(request):
    _session = request.GET.get('session', '')
    _token = request.GET.get('token', '')
    if _token == '' or _token == None:
        request.session['auth_source'] = "lotto"
        return HttpResponseRedirect(sina_utils.get_login_url())
   
    _player = Player.objects.get(token=_token)
    _today_has_shared_already = _is_the_same_date(_player.last_share_time, datetime.datetime.now())
    if _today_has_shared_already and _player.share_count >= 2:
        return HttpResponseRedirect(reverse('lotto_main')+'?session='+_session+'&token='+_token+'&ifc=0')
    #TODO: share to weibo
    _player.last_share_time = datetime.datetime.now()
    if _today_has_shared_already:
        _player.share_count += 1
    else:
        _player.share_count = 1
    _player.save()

    return HttpResponseRedirect(reverse('lotto_main')+'?session='+_session+'&token='+_token)

    

