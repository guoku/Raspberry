#encoding=utf8

from datetime import datetime 
from base.models import Entity
from django.db.models import Count,Sum
from user import date_format

class EntityStats(object):

    @classmethod 
    def new_entity_count(cls, start_time, end_time = datetime.now(), 
            category_id = None,neo_category_id = None, group = None):
        ##返回的数据格式：[{'count':12,'timestamp':"2012-01"}],date可能不存在
        _hd1 = Entity.objects.filter(created_time__range = (start_time,
            end_time))
        _hd1 = _hd1.filter(weight__gte = 0)

        if category_id != None:
            _hd1.filter(category__id = int(category_id))
        if neo_category_id != None:
            _hd1.filter(neo_category__id = int(neo_category_id))

        if group == None:
            count = _hd1.count()
            d = {'count':count}
            return [d]
        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"timestamp" : df}).values("timestamp")\
                    .annotate(count = Count('created_time'))
        return list(_hd1.all())


    @classmethod 
    def new_like_count(cls, start_time, end_time = datetime.now(),
            category_id = None, neo_category_id = None, group = None):
        _hd1 = Entity.objects.filter(created_time__range = (start_time, end_time))

        if category_id != None:
            _hd1 = _hd1.filter(category__id = category_id)

        if neo_category_id != None:
            _hd1 = _hd1.filter(neo_category__id = neo_category_id)

        if group == None:
            count = _hd1.aggregate(Sum('like_count'))['like_count__sum']
            d = {"count" : count}
            return [d]

        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"timestamp" : df}).values("timestamp")\
                    .annotate(count = Sum("like_count"))

        return list(_hd1.all())
