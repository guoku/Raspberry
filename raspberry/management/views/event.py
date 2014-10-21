from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import Show_Event_Banner, Event_Banner
from management.forms.event_banner import CreateEventBannerForms


def list(request, template='management/event/list.html'):

    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )

def create(request, template='management/event/create.html'):

    if request.method == "POST":
        _forms = CreateEventBannerForms(request.POST, request.FILES)
    else:
        _forms = CreateEventBannerForms()
    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


def edit(request, template=''):

    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
