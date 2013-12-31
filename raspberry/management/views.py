# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from banner import *
from category import *
#from entity import *
from note import *
from report import *
from user import *
from sync import *

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('management.views.entity_list', kwargs = {})) 
    else:
        return HttpResponseRedirect('admin')
        
        


