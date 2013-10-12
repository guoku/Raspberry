__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('mobile.views',
    url(r'^login/$', 'login'),
#    url(r'^logout/$', 'logout'),
    url(r'^register/$', 'register'),
    (r'^homepage/$', 'homepage'),
    (r'^entity/(?P<entity_id>\w+)/like/(?P<target_status>\d+)/$', 'like_entity'),
    (r'^category/$', 'all_category'),
    (r'^category/(?P<category_id>\d+)/entity/$', 'category_entity'),
)

