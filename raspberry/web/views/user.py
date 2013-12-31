# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from util import get_user_context


def likes(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )


def posts(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )


def notes(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )


def tags(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )


def followings(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )


def fans(request, user_id, template='user/user.html'):
    _user_context = get_user_context(request.user)

    return render_to_response(
        template,
        {
            'user_context' : _user_context
        },
        context_instance=RequestContext(request)
    )