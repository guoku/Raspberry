from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from utils.authority import staff_only
from base.models import Event
from base.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from management.forms.event import CreateEventForm
from django.utils.log import getLogger


log = getLogger('django')


@login_required
@staff_only
def list(request, template='management/event/list.html'):

    _page = request.GET.get('page', 1)
    event_list = Event.objects.all()

    paginator = ExtentPaginator(event_list, 30)

    try:
        events = paginator.page(_page)
    except PageNotAnInteger, e:
        events = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'events': events,
        },
        context_instance=RequestContext(request),
    )


def create(request, template='management/event/create.html'):

    if request.method == 'POST':
        _forms = CreateEventForm(request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = CreateEventForm()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance=RequestContext(request),
    )


def edit(request, eid, template='management/event/edit.html'):


    return render_to_response(
        template,
        {

        },
        context_instance=RequestContext(request),
    )

__author__ = 'edison'
