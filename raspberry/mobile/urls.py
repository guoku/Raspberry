__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('mobile.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^register/$', 'register'),
#    url(r'^weibo/register/$', 'register_by_weibo'),
#    url(r'^weibo/bind/$', 'bind_weibo'),
#    url(r'^weibo/unbind/$', 'unbind_weibo'),
)


