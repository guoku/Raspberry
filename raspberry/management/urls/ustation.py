from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.ustation',
    url(r'^$', 'ustation_list', name = 'management_ustation_list'),
    url(r'^random/$', 'ustation_random_generate', name = 'management_ustation_random_generate'),
    url(r'^clean/$', 'clean_ustation', name = 'management_clean_ustation'),
    url(r'^sync/$', 'sync_ustation', name = 'management_sync_ustation'),
)

