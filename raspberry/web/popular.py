# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.popularity import read_popular_entity_from_cache
from base.popularity import generate_popular_entity


def popular(request, template='popular/popular.html'):
    _group = request.GET.get('group', 'daily')

    generate_popular_entity()
    _entity_list = read_popular_entity_from_cache(_group)['data']

    print(_entity_list)

    return render_to_response(template,
        {

        },
        context_instance=RequestContext(request)
    )