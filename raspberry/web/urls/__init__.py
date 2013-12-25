from django.conf.urls.defaults import url, patterns, include

urlpatterns = patterns(
    '',
    ('^selection/$', 'web.views.main.selection'),
    (r'^popular/$', 'web.views.main.popular'),
    (r'^discover/$', 'web.views.main.discover'),
    (r'^detail/(?P<entity_hash>\w+)/$', 'web.views.main.detail'),

    ('^account/', include('web.urls.account')),

    # ('^note/', include('web.urls.note')),
    # ('^entity/', include('web.urls.entity')),
    # ('^user/', include('web.urls.user'))
)
