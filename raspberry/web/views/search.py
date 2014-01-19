# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
import json

from util import *


def search(request, template='search/search.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    _key_world = request.GET.get('keyword', None)

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
        },
        context_instance=RequestContext(request)
    )
