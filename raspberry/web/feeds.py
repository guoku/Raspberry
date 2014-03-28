from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
# from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _

from base.models import NoteSelection
from base.entity import Entity
from base.note import Note
from base.user import User
from datetime import datetime

class SelectionFeeds(Feed):
    title = _("guoku selection")
    link = '/selected/'
    description = ''

    def items(self):
        return NoteSelection.objects(post_time__lt = datetime.now())[:30]

    def item_title(self, item):
        _entity_id = item.entity_id
        _entity_context = Entity(_entity_id).read()
        return "%s - %s" %(_entity_context['brand'],_entity_context['title'])

    def item_link(self, item):
        _entity_id = item.entity_id
        _entity_context = Entity(_entity_id).read()
        return "/detail/%s/" % _entity_context['entity_hash']

    def item_description(self, item):
        _note_id = item.note_id
        _note_context = Note(_note_id).read()
        return "%s" % _note_context['content']

    def item_author_name(self, item):
        _note_id = item.note_id
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()
        return _creator_context['nickname']

    def item_pubdate(self, item):
        _note_id = item.note_id
        _note_context = Note(_note_id).read()
        return _note_context['post_time']

__author__ = 'edison7500'
