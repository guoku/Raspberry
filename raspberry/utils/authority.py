#coding=utf-8
from django.http import Http404

def staff_only(func=None):
    def staff_wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return func(request, *args, **kwargs)
    return staff_wrapped
