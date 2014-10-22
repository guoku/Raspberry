from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from base.models import Show_Event_Banner, Event_Banner
from management.forms.event_banner import CreateEventBannerForms, EditEventBannerForms


def list(request, template='management/event/list.html'):

    _show_banners = Show_Event_Banner.objects.all()
    _event_banners = Event_Banner.objects.all()
    return render_to_response(
        template,
        {
            'show_banners':_show_banners,
            'event_banners': _event_banners,
        },
        context_instance=RequestContext(request)
    )

def create(request, template='management/event/create.html'):

    if request.method == "POST":
        _forms = CreateEventBannerForms(request.POST, request.FILES)
        if _forms.is_valid():
            _event_banner = _forms.save()
            return HttpResponseRedirect(reverse('management_event_banner_edit', args=[_event_banner.id]))
    else:
        _forms = CreateEventBannerForms()
    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


def edit(request, event_banner_id, template='management/event/edit.html'):

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
