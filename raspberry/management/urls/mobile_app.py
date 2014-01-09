from django.conf.urls import url, patterns
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns(
    'management.views.mobile_app',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('management_app_list'))),
    url(r'^upload/$', 'upload_file', name = 'management_upload_app'),
    url(r'^list/$', 'app_list', name = 'management_app_list'),
    url(r'^(?P<pk>\d+)/pubilsh/$', 'publish_app', name = 'management_publish_app'),
)

__author__ = 'edison7500'
