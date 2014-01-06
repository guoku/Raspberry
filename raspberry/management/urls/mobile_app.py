from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.mobile_app',
    url(r'^upload/$', 'upload_file', name='management_upload_app'),
)

__author__ = 'edison7500'
