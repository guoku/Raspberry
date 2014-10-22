from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from base.models import Show_Editor_Recommendation, Editor_Recommendation
from management.forms.editor_recommendation import CreateEditorRecommendForms, EditEditorRecommendForms


def list(request, template='management/event/list.html'):

    _show_editor_recommendations = Show_Editor_Recommendation.objects.all()
    _editor_recommendations = Editor_Recommendation.objects.all()
    return render_to_response(
        template,
        {
            'show_editor_recommendations':_show_editor_recommendations,
            'editor_recommendations': _editor_recommendations,
        },
        context_instance=RequestContext(request)
    )

def create(request, template='management/event/create.html'):

    if request.method == "POST":
        _forms = CreateEditorRecommendForms(request.POST, request.FILES)
        if _forms.is_valid():
            _event_banner = _forms.save()
            return HttpResponseRedirect(reverse('management_event_banner_edit', args=[_event_banner.id]))
    else:
        _forms = CreateEditorRecommendForms()
    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


def edit(request, event_banner_id, template='management/event/edit.html'):

    try:
        _event_banner = Editor_Recommendation.objects.get(pk = event_banner_id)
    except Editor_Recommendation.DoesNotExist:
        raise Http404

    data = {
        # 'content_type': _banner.content_type,
        # 'key': _banner.key,
        'link': _event_banner.link,
        'position':_event_banner.position,

    }

    if request.method == "POST":
        _forms = EditEditorRecommendForms(_event_banner, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EditEditorRecommendForms(_event_banner, data=data)


    return render_to_response(
        template,
        {
            'event_banner':_event_banner,
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
