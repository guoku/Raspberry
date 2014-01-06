__author__ = 'edison'

import os
from django.conf import settings


APP_UPLOAD_DIR = getattr(settings, 'APP_UPLOAD_DIR', 'uploads/app/')


def handle_uploaded_file(f):
    if not os.path.exists(APP_UPLOAD_DIR):
        os.makedirs(APP_UPLOAD_DIR)
    file_path = APP_UPLOAD_DIR + 'guoku-release.apk'

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_app_location():

    return os.listdir(APP_UPLOAD_DIR)