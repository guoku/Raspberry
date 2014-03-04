from django.conf.urls import url, patterns

urlpatterns = patterns(
    'web.views.category',
    url(r'^(?P<cid>\d+)/$', 'category', name='web_category'),

)


__author__ = 'edison7500'
