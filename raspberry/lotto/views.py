# coding=utf8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.templatetags.static import static
from django.shortcuts import render_to_response
from mobile.lib.http import SuccessJsonResponse 
from mobile.models import Session_Key
from models import Accumulate, Player, Reward
from weibo import APIClient
from web import sina_utils
import datetime
import time
import os

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

def main(request, template='lotto.html'):
    _session = request.GET.get('session', '')
    _token = request.GET.get('token', '')
    _infocode = request.GET.get('ifc', None)
    _count = -1 
        

    _player = None
    if _token != '': 
        _player = Player.objects.get(token = _token)
    elif _session != '':
        _request_user_id = Session_Key.objects.get_user_id(_session)
        try:
            _player = Player.objects.get(user_id = _request_user_id)
            _token = _player.token
        except:
            pass
    
    if _player != None:
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

CURRENT_KEY = 1
def roll(request):
    _token = request.GET.get('token', None)
    _session = request.GET.get('session', None)
    _player = Player.objects.get(token=_token)
    _code = 0
    
    if not _is_the_same_date(_player.last_share_time, datetime.datetime.now()):
        return HttpResponseRedirect(reverse('lotto_share_to_sina_weibo') + '?session=' + _session + '&token=' + _token)
    
    if _player.share_count <= _player.roll_count:
        return SuccessJsonResponse({ 'code': 4 })

    try:
        _acc_obj = Accumulate.objects.get(key=CURRENT_KEY)
    except Accumulate.DoesNotExist:
        _acc_obj = Accumulate.objects.create(
            key=CURRENT_KEY,
            count=0
        )
    
    _acc_obj.count += 1
    if _acc_obj.count % 23 == 0:
        if Reward.objects.filter(level=1).count() < 15:
            _code = 1
            Reward.objects.create(
                player_id=_player.id,
                level=1
            )
    elif _acc_obj.count % 31 == 0:
        if Reward.objects.filter(level=2).count() < 25:
            _code = 2
            Reward.objects.create(
                player_id=_player.id,
                level=2
            )
    elif _acc_obj.count % 43 == 0:
        if Reward.objects.filter(level=3).count() < 15:
            _code = 3
            Reward.objects.create(
                player_id=_player.id,
                level=3
            )
        
    _acc_obj.save()
    _player.roll_count += 1
    _player.save()

    _left_roll_count = _player.share_count - _player.roll_count
    
    return SuccessJsonResponse({ 
        'code' :  _code,
        'leftrollcount' : str(_left_roll_count) 
    })
     
def share_to_sina_weibo(request):
    _session = request.GET.get('session', '')
    _token = request.GET.get('token', '')
    
    if _token == '' or _token == None:
        request.session['auth_source'] = 'lotto'
        if _session != '':
            request.session['mobile_session'] = _session 
        return HttpResponseRedirect(sina_utils.get_login_url())
    
    _player = Player.objects.get(token=_token)
    
    _timestamp = datetime.datetime.fromtimestamp(float(_player.expires_in))
    if _timestamp <= datetime.datetime.now():
        request.session['auth_source'] = 'lotto'
        if _session != '':
            request.session['mobile_session'] = _session 
        return HttpResponseRedirect(sina_utils.get_login_url())

    _today_has_shared_already = _is_the_same_date(_player.last_share_time, datetime.datetime.now())
    if _today_has_shared_already and _player.share_count >= 2:
        return HttpResponseRedirect(reverse('lotto_main')+'?session='+_session+'&token='+_token+'&ifc=0')
    
    pic_f = open(os.path.dirname(os.path.realpath(__file__)) + '/iphone.png', 'rb') 
    sina_utils.post_weibo(_player.access_token, _player.expires_in, u'衣带渐宽徒伤悲，唯曼妙身材与健康体格不可辜负，即日起，登录「果库」客户端即有机会获得瘦身神器 —— @云悦智能体质分析仪。通过「果库」客户端分享活动至新浪微博，更有机会赢取多一次抽奖机会！戳 → http://www.guoku.com/lotto/', pic_f) 
    
    _player.last_share_time = datetime.datetime.now()
    if _today_has_shared_already:
        _player.share_count += 1
    else:
        _player.share_count = 1
        _player.roll_count = 0
    _player.save()

    return HttpResponseRedirect(reverse('lotto_main')+'?session='+_session+'&token='+_token+'&ifc=1')

    
def guoku_generation_3_activity(request, template='activity.html'):
    return render_to_response(
        template, 
        {
        }, 
        context_instance=RequestContext(request)
    )

