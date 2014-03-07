from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.log import getLogger



log = getLogger('django')

def tags(request, tag_hash, template="tags/tags.html"):

    return render_to_response(template,
        {

        },
        context_instance = RequestContext(request))

__author__ = 'edison7500'
