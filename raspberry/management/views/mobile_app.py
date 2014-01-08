from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect

from management.forms.mobile_app import UploadFileForm
from management.lib.handle_uploaded_file import handle_uploaded_file
from management.models import App_Pubilsh
from management.tasks import PublishApkTask

@login_required
def upload_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('management_app_list'))
    else:
        form = UploadFileForm()
    
    return render_to_response(
        'mobile_app/upload_app.html',
        {
            'form' : form
        },
        context_instance = RequestContext(request)
    )


@login_required
def app_list(request):
    # app_list = get_app_location()
    app_list = App_Pubilsh.objects.all()

    return render_to_response( 
        'mobile_app/app_list.html',
        {
            'apps' : app_list
        },
        context_instance = RequestContext(request)
    )


@login_required
def publish_app(request, pk):
    app = App_Pubilsh.objects.get(pk = pk)

    r = PublishApkTask()
    try:
        r.run(filename = app.file)
        app.is_published = True
        app.save()
        return HttpResponseRedirect(reverse('management_app_list'))
    except Exception:
        raise
__author__ = 'edison7500'
