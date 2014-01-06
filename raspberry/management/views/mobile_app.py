from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from management.forms.mobile_app import UploadFileForm

@login_required
def upload_file(request):

    if request.method == 'POST':

        return
    else:
        form = UploadFileForm()
        return render_to_response('mobile_app/upload_app.html',
                                  {'form': form},
                                context_instance=RequestContext(request))

__author__ = 'edison7500'
