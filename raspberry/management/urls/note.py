from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.note',
    url(r'^$', 'note_list', name = 'management_note_list'),
    url(r'^arrange/selection/$', 'arrange_selection', name = 'management_arrange_selection'),
    url(r'^(?P<note_id>\w+)/edit/$', 'edit_note', name = 'management_edit_note'),
    url(r'^(?P<note_id>\w+)/freeze/$', 'freeze_note', name = 'management_freeze_note'),
)

__author__ = 'edison7500'
