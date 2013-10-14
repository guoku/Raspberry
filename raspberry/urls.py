__author__ = 'stxiong'
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'management.views.index'),
    (r'^management/', include('management.urls')),
    (r'^api/v1/', include('mobile.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:

    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
