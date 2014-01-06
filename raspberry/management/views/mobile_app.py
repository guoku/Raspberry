from management.forms.mobile_app import UploadFileForm
from django.shortcuts import render_to_response

def upload_file(request):

    if request.method == 'POST':

        return
    else:
        form = UploadFileForm()
        return render_to_response('mobile_app/upload_app.html',
                                  {'form':form})

__author__ = 'edison7500'
