#encoding=utf-8
from datetime import datetime 
from base.models import Note as NoteModel
from base.models import Note_Comment as CommentModel
from base.models import Note_Poke as PokeModel
from user import date_format
from django.db.models import Count
class NoteStats(object):

    @classmethod 
    def new_note_count(cls,start_time,end_time = datetime.now(), entity_id=None, group = None):
        ##返回的数据格式：[{'count':12,'date':"2012-01"}],date可能不存在
        _hd1 = NoteModel.objects.filter(created_time__range = 
                                        (start_time, end_time))
        if entity_id != None:
            _hd1 = _hd1.filter(entity__id = int(entity_id))
        if group == None:
            count = _hd1.count()
            d = {"count":count}
            return [d]
        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"date" : df}).values("date")\
                    .annotate(count = Count('created_time'))
        return list(_hd1.all())
    
    @classmethod
    def new_poke_count(cls, start_time, end_time = datetime.now(),
                        group = None):
        _hd1 = PokeModel.objects.filter(created_time__rane = 
                                    (start_time, end_time))
        if group == None:
            count = _hd1.count()
            d = {"count" : count}
            return [d]
        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"date" : df})\
                    .values("date").annotate(count = Count("created_time"))

        return list(_hd1.all())

    @classmethod
    def new_note_comment(cls, start_time, end_time = datetime.now(),
                            group = None):
        _hd1 = CommentModel.objects.filter(created_time__range = \
                (start_time, end_time))

        if group == None:
            count = _hd1.count()
            d = {"count" : count}
            return [d]

        else:
            group = group.lower()
            df = date_format("created_time", group)
            _hd1 = _hd1.extra(select = {"date" : df})\
                    .values("date").annotate(count = Count("created_time"))

        return list(_hd1.all())
