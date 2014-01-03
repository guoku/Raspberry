__author__ = 'edison7500'

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('entity_list', kwargs = {}))
    else:
        return HttpResponseRedirect('admin')