__author__ = 'stxiong'
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.contrib import admin
admin.autodiscover()

handler500 = 'web.views.page_error'
handler404 = 'web.views.webpage_not_found'
handler403 = 'django.views.defaults.permission_denied'

urlpatterns = patterns('',
    (r'^management/', include('management.urls')),
    (r'^seller/', include('seller.urls')),
    (r'^mobile/v3/', include('mobile.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^stats/', include('stats.urls')),
#    (r'^lotto/', include('lotto.urls')),
    (r'', include('web.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^403/$', 'django.views.defaults.permission_denied'),
    url(r'^404/$', 'web.views.webpage_not_found'),
    url(r'^500/$', 'web.views.page_error'),
    (r'^visit_item/$', 'mobile.views.old_visit_item'),
)

if settings.IMAGE_LOCAL:
    urlpatterns += patterns('',
        (r'^image/local/avatar/(?P<size>\w+)/(?P<key>\w+)$', 'base.views.local_avatar_image'),
        (r'^image/local/img/(?P<key>\w+).(?P<image_format>\w+)$', 'base.views.local_entity_image'),
        (r'^image/local/img/(?P<key1>\w+).(?P<key2>\w+).(?P<key3>\w+)$', 'base.views.local_entity_image_extend'),
        (r'^image/local/category/(?P<key1>\w+)/(?P<key2>\w+)$', 'base.views.local_category_image'),
    )


#if settings.DEBUG:
    #import debug_toolbar
    #urlpatterns += patterns('',
    #    url(r'^__debug__/', include(debug_toolbar.urls)),
    #)

    #urlpatterns += patterns('',
    #  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #)

    #urlpatterns += patterns('',
    #    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
    #        {'document_root': settings.MEDIA_URL}),
    #)
