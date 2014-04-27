# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from base.user import User


def download(request):
    _user_agent = request.META['HTTP_USER_AGENT']
    if 'iPhone' in _user_agent :
        _download_url = 'https://itunes.apple.com/cn/app/id477652209'
    elif 'iPad' in _user_agent :
        _download_url = 'https://itunes.apple.com/cn/app/id450507565'
    elif 'Android' in _user_agent :
        _download_url = 'http://app.guoku.com/download/android/guoku-release.apk'
    else:
        _download_url = "http://guoku.com/"
    return HttpResponseRedirect(_download_url)

def download_ios(request, template="download_ios.html"):
    if request.user.is_authenticated():
        _request_user_context = User(request.user.id).read() 
    else:
        _request_user_context = None
    
    return render_to_response(
        template,
        {   
            'user_context' : _request_user_context,
        },
        context_instance = RequestContext(request)
    )
