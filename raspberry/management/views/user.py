#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from management.tasks import FreezeUserEntityNoteAll, PushMessageToUserTask


from base.user import User
from utils.authority import staff_only 
from utils.paginator import Paginator
from management.forms.user import UserForms
import logging
logger = logging.getLogger('django.request')

@login_required
@staff_only
def user_list(request, template='user/list.html'):
    _page_num = int(request.GET.get("p", "1"))
    _user_count = User.count()
    _paginator = Paginator(_page_num, 30, _user_count)
    _user_id_list = User.find(
        offset = _paginator.offset,
        count = _paginator.count_in_one_page,
    )
        
    _context_list = []
    for _user_id in _user_id_list:
        try:
            _user = User(_user_id)
            _user_context = _user.read()
            _context_list.append(_user_context)
        except Exception, e:
            pass
        
    return render_to_response( 
        template,
        {
            'active_division' : 'user',
            'context_list' : _context_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )


@login_required
@staff_only
def edit_user(request, user_id, template='user/edit.html'):
    if request.method == 'POST':
        # _user = User(user_id)
        forms = UserForms(request.POST)
        if forms.is_valid():
            forms.update(user_id)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return render_to_response(
                template,
                {
                    'forms': forms,
                    'user_context': User(user_id).read(with_censor=False),
                },
                context_instance = RequestContext(request)
            )
    else:
        _user_context = User(user_id).read(with_censor=False)
        forms = UserForms(initial=_user_context)
        return render_to_response(
            template,
            {
                'forms': forms,
                'user_context': _user_context,
            },
            context_instance = RequestContext(request)
        )

@login_required
@staff_only
def push_message_to_user(request, user_id):
    if request.method == 'POST':
        _user_id = int(user_id)
        _badge = int(request.POST.get("badge", "1"))
        _message = request.POST.get("message", None)
        
        PushMessageToUserTask.delay(
            user_id = _user_id,
            badge = _badge,
            message = _message,
            testor_id = request.user.id,
        )
        
        return HttpResponseRedirect(request.META['HTTP_REFERER'] + "?apns=1")


@login_required
@staff_only
def freeze_user_note_all(request, user_id):
    _user_id = int(user_id)
    FreezeUserEntityNoteAll.delay(
        user_id = _user_id,
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@staff_only
def set_censor(request, user_id):
    _censor_id = request.user.id
    User(user_id).set_censor(_censor_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@staff_only
def cancel_censor(request, user_id):
    _censor_id = request.user.id
    User(user_id).cancel_censor(_censor_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
