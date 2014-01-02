from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',
    url(r'^category/sync/$', 'management.views.sync.sync_category', name='sync_category'),
    url(r'^entity/create/offline/$', 'management.views.sync.create_entity_from_offline', name='create_entity_from_offline'),

    url(r'^category/', include('management.urls.category')),
    url(r'^entity/', include('management.urls.entity')),
    url(r'^note/', include('management.urls.note')),
    url(r'^user/', include('management.urls.user')),

)

__author__ = 'edison7500'
