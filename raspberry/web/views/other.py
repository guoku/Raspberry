# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from base.user import User

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
