from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import Show_Event_Banner, Event_Banner

def list(request, template='management/event/list.html'):

    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )

def create(request, template='management/event/create.html'):


    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
