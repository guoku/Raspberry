from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
# from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _
from django.utils.feedgenerator import Rss201rev2Feed

from base.models import NoteSelection
from base.entity import Entity
from base.note import Note
from base.user import User
from datetime import datetime

class CustomFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"image", item['image'])
        # handler.addQuickElement(u"short_description", item['short_description'])

class SelectionFeeds(Feed):
    feed_type = CustomFeedGenerator

    title = _("guoku selection")
    link = '/selected/'
    description = _('guoku selection desc')

    description_template = "feeds/selection_description.html"

    def items(self):
        return NoteSelection.objects(post_time__lt = datetime.now())[:60]

    def item_title(self, item):
        _entity_id = item.entity_id
        _entity_context = Entity(_entity_id).read()
        if len(_entity_context['brand']) > 0:
            return "%s - %s" % (_entity_context['brand'],_entity_context['title'])
        return _entity_context['title']

    def item_link(self, item):
        _entity_id = item.entity_id
        _entity_context = Entity(_entity_id).read()
        # return "/detail/%s/" % _entity_context['entity_hash']
        return reverse('web_detail', args=[_entity_context['entity_hash']])

    # def item_description(self, item):
    #     _note_id = item.note_id
    #     _note_context = Note(_note_id).read()
    #     return _note_context['content']

    def item_author_name(self, item):
        _note_id = item.note_id
        _note_context = Note(_note_id).read()
        _creator_context = User(_note_context['creator_id']).read()
        return _creator_context['nickname']

    def item_pubdate(self, item):
        _note_id = item.note_id
        _note_context = Note(_note_id).read()
        return _note_context['post_time']

    def item_extra_kwargs(self, item):
        _entity_id = item.entity_id
        _entity_context = Entity(_entity_id).read()
        return {'image':_entity_context['chief_image']['url']}

__author__ = 'edison7500'
