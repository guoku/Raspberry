from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
# from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _
from base.models import NoteSelection
from datetime import datetime

class SelectionFeeds(Feed):
    title = _("guoku selection")
    link = '/selected/'
    description = ''

    def items(self):
        return NoteSelection.objects(post_time__lt = datetime.now())

    def item_title(self, item):
        _entity_id = item['entity_id']

__author__ = 'edison7500'
