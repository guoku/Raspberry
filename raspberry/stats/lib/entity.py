#encoding=utf8

from datetime import datetime 
from base.models import Entity
from django.db.models import Count
from user import date_fromat

class EntityStats(object):

    @classmethod 
    def new_entity_count(cls, start_time, end_time = datetime.now(), 
            category_id = None,neo_category_id = None, group = None):
        ##返回的数据格式：[{'count':12,'date':"2012-01"}],date可能不存在
        _hd1 = Entity.objects.filter(created_time__range = (start_time,
            end_time))
        _hd1 = _hd1.filter(weight__gte = 0)

        if category_id != None:
            _hd1.filter(category_id = int(category_id))
        if neo_category_id != None:
            _hd1.filter(neo_category_id = int(neo_category_id))

        if group == None:
            count = _hd1.count()
            d = {'count':count}
            return [d]
        else:
            group = group.lower()
            df = date_fromat("created_time", group)
            _hd1.extra(select = {"date" : df}).values("date")\
                    .annotate(count = Count('created_time'))
        return list(_hd1.all())
