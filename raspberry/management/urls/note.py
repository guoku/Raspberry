from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.note',
    url(r'^$', 'note_list', name='note_list'),
    url(r'^arrange/selection/$', 'arrange_selection', name='arrange_selection'),
    url(r'^(?P<note_id>\w+)/edit/$', 'edit_note', name='note_edited'),
    url(r'^(?P<note_id>\w+)/freeze/$', 'freeze_note', name='note_freezed'),
)

__author__ = 'edison7500'
