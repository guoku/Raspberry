__author__ = 'stxiong'
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'lotto.views',
    url(r'^$', 'main', name='lotto_main'),
    url(r'^roll/$', 'roll', name='lotto_roll'),
    url(r'^share/$', 'share_to_sina_weibo', name='lotto_share_to_sina_weibo'),
)

