# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from util import get_request_user_context
from base.user import User


def index(request, user_id):
    return likes(request, user_id)


def likes(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 1,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def posts(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 2,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def notes(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 3,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def tags(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 4,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def followings(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 5,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )


def fans(request, user_id, template='user/index.html'):
    _user_context = get_request_user_context(request.user)
    _query_user = User(user_id)
    _query_user_context = _query_user.read()

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'content_tab' : 6,
            'query_user_context' : _query_user_context
        },
        context_instance=RequestContext(request)
    )