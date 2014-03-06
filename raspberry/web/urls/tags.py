from django.conf.urls import url, patterns

urlpatterns = patterns(
    'web.views.tags',
    url(r'^(?P<tag_hash>\w+)/$', 'tags', name='web_tags'),

)


__author__ = 'edison7500'
