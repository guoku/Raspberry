# coding=utf-8
from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    'web.views.main',
    url('^selected/$', 'selection', name='web_selection'),
    url('^popular/$', 'popular', name='web_popular'),
    url('^discover/$', 'discover', name='web_discover'),
    url('^discover/product/$', 'discover_more', name='web_discover_more'),
    url('^detail/(?P<entity_hash>\w+)/$', 'detail', name='web_detail'),

    url('^shop/(?P<shop_id>\w+)/$', 'shop', name='web_shop'),
    url('^message/$', 'message', name='web_message'),
    url('^activity/$', 'activity', name='web_activity'),

    url(r'^account/', include('web.urls.account')),
    url(r'^u/', include('web.urls.user')),
    url(r'^entity/', include('web.urls.entity')),
    url(r'^note/', include('web.urls.note')),
)


urlpatterns += patterns(
    'web.views.search',
    url('^search/$', 'search', name='web_search')
)