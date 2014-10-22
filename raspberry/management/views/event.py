from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import Show_Event_Banner, Event_Banner
from management.forms.event_banner import CreateEventBannerForms, EditEventBannerForms


def list(request, template='management/event/list.html'):

    _show = Show_Event_Banner.objects.all()

    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request)
    )

def create(request, template='management/event/create.html'):

    if request.method == "POST":
        _forms = CreateEventBannerForms(request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()

    else:
        _forms = CreateEventBannerForms()
    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


def edit(request, event_banner_id, template=''):

    try:
        _event_banner = Event_Banner.objects.get(pk = event_banner_id)
    except Event_Banner.DoesNotExist:
        raise Http404


    if request.method == "POST":
        _forms = EditEventBannerForms(_event_banner, request.POST, request.FILES)
    else:
        _forms = EditEventBannerForms(_event_banner)


    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
