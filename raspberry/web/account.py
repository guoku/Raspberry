#coding=utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response 
from urlparse import urlparse
from base.user import User
from web import taobao_utils
from web import web_utils
from utils import fetcher
@login_required
def bind_taobao(request):
    request.session['bind_taobao_next_url'] = request.GET.get('next', None)
    request.session['back_to_url'] = reverse('web.views.bind_taobao_check')
    return HttpResponseRedirect(taobao_utils.get_login_url())

def taobao_auth(request):
    return HttpResponseRedirect(taobao_utils.auth(request))

def bind_taobao_check(request):
    access_token = request.session['taobao_access_token']
    taobao_id = request.session['taobao_id']
    expires_in = int(time.time()) + int(request.session['taobao_expires_in'])

    taobao_user = taobao_utils.get_taobao_user_info(access_token_)
    user_id = request.user.id
    user_inst = User(user_id)
    if taobao_user:
        try:
            user_inst.bind_taobao(taobao_id, taobao_user['nick'], access_token, expires_in)
            if request.session.get('bind_taobao_next_url', None):
                next_url = request.session['bind_taobao_next_url']
                try:
                    del request.session['bind_taobao_next_url']
                except KeyError:
                  return HttpResponseRedirect(request.META['HTTP_REFERER'])
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except User.TaobaoIdExistAlready, e:
            pass
        except User.UserBindTaobaoAlready, e:
            pass
        except Exception, e:
            pass
    else:
        HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bind_taobao_shop(request):
    user_id = request.user.id
    user_inst = User(user_id)
    request_user_context = user_inst.read()
    if request.method == "GET":
        if request_user_context.get("taobao_screen_name"):
            if request_user_context['taobao_token_expires_in'] < time.time():
                request_user_context['taobao_token_expired'] = True
            else:
                request_user_context['taobao_token_expired'] = False
       return render_to_response( "bind_taobao_shop.html",
                                  { "request_user_context" : request_user_context },
                                  context_instance=RequestContext(request)
                                )
    elif request.method == "POST":
        if not request_user_context.get("taobao_nick"):
            #message
            return HttpResponseRedirect(reverse('web.views.bind_taobao_shop'))
        item_url = request.POST.get('item_url', None)
        if not item_url:
            return HttpResponseRedirect(reverse('web.views.bind_taobao_shop'))
      
        hostname = urlparse(item_url).hostname
        if re.search(r"\b(tmall|taobao)\.(com|hk)$", hostname) != None:
            taobao_id = web_utils.parse_taobao_id_from_url(item_url)
            taobao_item_info = fetcher.fetch(taobao_id)
            if request_user_context.get('taobao_nick') == taobao_item_info['nick']:
                user_inst.create_seller_info(taobao_item_info['nick'])
                # query shop, if not exist, add it
                return HttpResponseRedirect(reverse('web.views.bind_taobao_shop'))
            else:
                return HttpResponseRedirect(reverse('web.views.bind_taobao_shop'))
        else:
            return HttpResponseRedirect(reverse('web.views.bind_taobao_shop'))

    
