from django.conf.urls.defaults import *

urlpatterns = patterns('web.views',
                       (r'^selection/$', 'selection'),
                       (r'^detail/(?P<entity_id>\w+)/$', 'detail'))


