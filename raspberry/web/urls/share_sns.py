from django.conf.urls import url, patterns
from web.views.share_sns import WeiboView

urlpatterns = patterns(
    'web.views.share_sns',
    url(r'^weibo/$', WeiboView.as_view(), name='web_share_weibo'),
)

__author__ = 'edison7500'
