#encoding=utf8

from datetime import datetime
from base.models import Entity_Tag as ETagModel 
from user import date_format
from django.db.models import Count
class TagStats(object):

    @classmethod
    def new_tag_count(cls, start_time, end_time = datetime.now(),
                        creator_id = None, group = None):
        _hd1 = ETagModel.objects.filter(created_time__range = (start_time,
            end_time))
        if creator_id != None:
            _hd1 = _hd1.filter(user__id = creator_id)

        if group == None:
            count = _hd1.count()
            d = {"count" : count}
            return [d]
        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"timestamp" : df}).values("timestamp")\
                    .annotate(count = Count('created_time'))
            
            result = list(_hd1.all())
            if group == "week":
                result = week_reformat(result)
            return result
