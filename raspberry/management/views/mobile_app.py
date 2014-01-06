from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect

from management.forms.mobile_app import UploadFileForm
from management.lib.handle_uploaded_file import handle_uploaded_file, get_app_location

@login_required
def upload_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print dir(form)
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('management_publish_app'))
    else:
        form = UploadFileForm()
    return render_to_response('mobile_app/upload_app.html',
                                  {'form': form},
                                context_instance=RequestContext(request))


@login_required
def publish_app(request):
    app_list = get_app_location()
    return render_to_response( 'mobile_app/app_list.html',
        {'apps': app_list},
        context_instance=RequestContext(request)
    )

__author__ = 'edison7500'
