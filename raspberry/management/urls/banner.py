from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.banner',
    url(r'^$', 'banner_list', name='banner_list'),
)

__author__ = 'edison7500'
