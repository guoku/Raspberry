#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseBadRequest
import HTMLParser
import re 
import datetime
import time
import json

from base.banner import Banner
from base.models import Banner as BannerModel 
from utils.authority import staff_only 
from utils.paginator import Paginator

# from management.forms.banner import CreateBannerForm



@login_required
@staff_only
def banner_list(request):
    _page_num = int(request.GET.get("p", "1"))
    _paginator = Paginator(_page_num, 30, BannerModel.objects.count())
    
    _banner_context_list = Banner.find(
        offset = _paginator.offset,
        count = _paginator.count_in_one_page
    )
    
    return render_to_response( 
        'banner/list.html', 
        {
            'active_division' : 'banner',
            'banner_context_list' : _banner_context_list,
            'paginator' : _paginator
        },
        context_instance = RequestContext(request)
    )

@login_required
@staff_only
def new_banner(request, template="management/banner/create.html"):

    # if request.method == "POST":
    #     _forms = CreateBannerForm(request.POST, request.FILES)
    #     if _forms.is_valid():
    #         _forms.save()
    #         return HttpResponseRedirect(reverse('management_banner_list'))
    # else:
    #     _forms = CreateBannerForm()
    # return render_to_response(
    #     template,
    #     {
    #         'forms': _forms,
    #
    #     },
    #     context_instance=RequestContext(request),
    # )
    if request.method == 'GET':
        _content_type_list = ['entity', 'category', 'user', 'user_tag', 'outlink']
        return render_to_response(
            'banner/new.html',
            {
                'active_division' : 'banner',
                'content_type_list' : _content_type_list
            },
            context_instance=RequestContext(request)
        )

@login_required
@staff_only
def create_banner(request):
    if request.method == 'POST':
        _content_type = request.POST.get("content_type", None)
        _key = request.POST.get("key", None)
        _weight = int(request.POST.get("weight", "0"))
        
        _image_file = request.FILES.get('image', None)
        _image_data = None
        if _image_file != None:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        
        _banner_id = Banner.create(
            key = _key,
            content_type = _content_type,
            image_data = _image_data,
            weight = _weight
        )
        return HttpResponseRedirect(reverse('management_banner_list'))
    else:
        return HttpResponseBadRequest()


@login_required
@staff_only
def edit_banner(request, banner_id):
    if request.method == 'GET':

        _banner_context = Banner(banner_id).read()

        return render_to_response(
            'banner/edit.html', 
            {
                'active_division' : 'banner',
                'banner_context' : _banner_context
            },
            context_instance = RequestContext(request)
        )
    else:
        _weight = request.POST.get("weight", None)
        Banner(banner_id).update(_weight)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@staff_only
def delete_banner(request, banner_id):
    Banner(banner_id).delete()
    return HttpResponseRedirect(reverse('management_banner_list'))
