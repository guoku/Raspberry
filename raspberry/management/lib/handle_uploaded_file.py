__author__ = 'edison'

import os
from django.conf import settings
from management.models import App_Pubilsh

APP_UPLOAD_DIR = getattr(settings, 'APP_UPLOAD_DIR', 'uploads/app/')


def handle_uploaded_file(f):
    # print os.getcwd()
    if not os.path.exists(APP_UPLOAD_DIR):
        os.makedirs(APP_UPLOAD_DIR)
    file_path = APP_UPLOAD_DIR + f.name
    with open(file_path, 'wb+') as destination:
        for chuck in f.chunks():
            destination.write(chuck)


    try:
        app = App_Pubilsh.objects.get(name = f.name)
        # app.name = f.name
        app.file = file_path
    # app.file.save(f.name, f, save=True)
        app.save()
    except App_Pubilsh.DoesNotExist, e:
        app = App_Pubilsh()
        app.name = f.name
        app.file = file_path
        app.save()
    # for chunk in f.chunks():
    #     print chunk
    # if not os.path.exists(APP_UPLOAD_DIR):
    #     os.makedirs(APP_UPLOAD_DIR)
    # file_path = APP_UPLOAD_DIR + 'guoku-release.apk'
    #
    # with open(file_path, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)


# def get_app_location():
#
#     return os.listdir(APP_UPLOAD_DIR)