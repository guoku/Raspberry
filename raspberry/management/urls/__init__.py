from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',
    url(r'^category/sync/$', 'management.views.sync.sync_category', name='sync_category'),
    url(r'^entity/create/offline/$', 'management.views.sync.create_entity_from_offline', name='create_entity_from_offline'),

    url(r'^category/', include('management.urls.category')),
    url(r'^entity/', include('management.urls.entity')),
    url(r'^note/', include('management.urls.note')),
    url(r'^banner/', include('management.urls.banner')),
    url(r'^user/', include('management.urls.user')),
    url(r'report/', include('management.urls.report')),

)

__author__ = 'edison7500'
