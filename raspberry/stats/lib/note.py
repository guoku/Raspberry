#encoding=utf-8
from datetime import datetime 
from base.models import Note as NoteModel
from user import date_fromat
class NoteStats(object):

    @classmethod 
    def new_note_count(cls,start_time,end_time = datetime.now(), entity_id=None, group = None):
        ##返回的数据格式：[{'count':12,'date':"2012-01"}],date可能不存在
        _hd1 = NoteModel.objects.filter(created_time__range = 
                                        (start_time, end_time))
        if entity_id != None:
            _hd1.NoteModel.objects.filter(entity_id = int(entity_id))
        if group == None:
            count = _hd1.count()
            d = {"count":count}
            return [d]
        else:
            group = group.lower()
            df = date_fromat("created_time",group)
            _hd1.extra(select = {"date" : df}).values("date")\
                    .annotate(available = Count('created_time'))
        return list(_hd1.all())
